import pytest
import os
from fastapi.testclient import TestClient
from app.main import app
from app.pipeline.validator import RecordValidator
from app.pipeline.normalizer import RecordNormalizer
from app.pipeline.deduplicator import RecordDeduplicator
from app.pipeline.quality import DataQualityScorer
from app.scraper.rate_limiter import RateLimiter
from app.scraper.coa_adapter import CoADirectoryAdapter
from app.scraper.mock_adapter import MockDirectoryAdapter
from app.database.session import SessionLocal

client = TestClient(app)

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "Council of Architecture" in data["message"]

def test_config_endpoint():
    response = client.get("/api/config")
    assert response.status_code == 200
    data = response.json()
    assert "coa_base_url" in data
    assert "max_concurrency" in data

def test_record_validator():
    # Valid record
    valid_record = {
        "registration_number": "CA/1975/00005",
        "name": "Mr. N.T. Venkatesh",
        "valid_up_to": "31/12/1979"
    }
    is_valid, err = RecordValidator.validate(valid_record)
    assert is_valid is True
    assert err is None

    # Invalid record (missing name)
    invalid_record = {
        "registration_number": "CA/1975/00005",
        "name": ""
    }
    is_valid, err = RecordValidator.validate(invalid_record)
    assert is_valid is False

    # Invalid registration number
    invalid_reg = {
        "registration_number": "XYZ123",
        "name": "Test Architect"
    }
    is_valid, err = RecordValidator.validate(invalid_reg)
    assert is_valid is False

def test_record_normalizer():
    raw_record = {
        "registration_number": "ca/1975/00005",
        "name": "mr. n.t.  venkatesh",
        "city": "bengaluru",
        "valid_up_to": "31/12/1979"
    }
    norm = RecordNormalizer.normalize(raw_record)
    assert norm["registration_number"] == "CA/1975/00005"
    assert norm["name"] == "Mr. N.T. Venkatesh"
    assert norm["city"] == "Bengaluru"
    assert norm["state"] == "Karnataka"  # Auto inferred
    assert norm["registration_year"] == 1975
    assert norm["status"] == "Inactive"  # Valid up to 1979 is expired

def test_deduplicator():
    db = SessionLocal()
    try:
        dedup = RecordDeduplicator(db)
        record = {
            "registration_number": "CA/2020/99999",
            "name": "Ar. Test Architect",
            "city": "Mumbai"
        }
        # First time: not duplicate
        assert dedup.is_duplicate(record) is False
        # Second time: is duplicate
        assert dedup.is_duplicate(record) is True
    finally:
        db.close()

def test_data_quality_scorer():
    records = [
        {
            "registration_number": "CA/1975/00005",
            "name": "Mr. N.T. Venkatesh",
            "city": "Bengaluru",
            "state": "Karnataka",
            "valid_up_to": "31/12/1979",
            "registration_year": 1975
        },
        {
            "registration_number": "CA/2021/12345",
            "name": "Ar. Priya Sharma",
            "city": "Mumbai",
            "state": "Maharashtra",
            "valid_up_to": "31/12/2026",
            "registration_year": 2021
        }
    ]
    report = DataQualityScorer.score_dataset(records, duplicate_count=0)
    assert report["overall_score"] > 90.0
    assert report["completeness"] == 100.0
    assert report["validity"] == 100.0
    assert report["uniqueness"] == 100.0

@pytest.mark.asyncio
async def test_rate_limiter():
    limiter = RateLimiter(requests_per_second=10.0, max_concurrency=2)
    await limiter.acquire()
    assert limiter.tokens >= 0.0
    limiter.report_rate_limited(retry_after=0.1)
    assert limiter.consecutive_429_count == 1
    limiter.report_success()
    assert limiter.consecutive_429_count == 0

@pytest.mark.asyncio
async def test_mock_adapter():
    limiter = RateLimiter(requests_per_second=20.0, max_concurrency=5)
    adapter = MockDirectoryAdapter(rate_limiter=limiter, simulated_delay=0.0)
    page_html = await adapter.fetch_page(1)
    records = adapter.parse_records(page_html)
    assert len(records) > 0
    assert "registration_number" in records[0]
    assert "name" in records[0]

def test_coa_adapter_parser():
    # Test with real saved HTML from Council of Architecture
    html_path = os.path.join(os.path.dirname(__file__), "..", "..", "scratch", "default_arch.php.html")
    if os.path.exists(html_path):
        with open(html_path, "r", encoding="utf-8") as f:
            html = f.read()
        limiter = RateLimiter(requests_per_second=1.0)
        adapter = CoADirectoryAdapter(rate_limiter=limiter)
        records = adapter.parse_records(html)
        assert len(records) >= 50
        assert records[0]["registration_number"] == "CA/1975/00005"
        assert "VENKATESH" in records[0]["name"].upper()
        assert records[0]["city"] == "Bengaluru"

def test_job_creation_and_api():
    payload = {
        "start_page": 1,
        "end_page": 2,
        "concurrency": 2,
        "requests_per_second": 5.0,
        "timeout_seconds": 15,
        "retry_count": 2,
        "mode": "mock"
    }
    response = client.post("/api/jobs", json=payload)
    assert response.status_code == 200
    job_data = response.json()
    assert "id" in job_data
    assert job_data["status"] in ["PENDING", "RUNNING", "COMPLETED"]

    # List jobs
    resp_list = client.get("/api/jobs")
    assert resp_list.status_code == 200
    jobs = resp_list.json()
    assert len(jobs) > 0

    # Get single job
    resp_single = client.get(f"/api/jobs/{job_data['id']}")
    assert resp_single.status_code == 200

def test_directory_and_analytics_endpoints():
    # Directory listing
    resp = client.get("/api/directory/architects?page=1&page_size=10")
    assert resp.status_code == 200
    data = resp.json()
    assert "total" in data
    assert "items" in data

    # Analytics summary
    resp_analytics = client.get("/api/analytics")
    assert resp_analytics.status_code == 200
    analytics_data = resp_analytics.json()
    assert "total_records" in analytics_data
    assert "states_distribution" in analytics_data
    assert "data_quality_score" in analytics_data
