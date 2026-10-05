import asyncio
import time
import sys
import os
import tracemalloc

# Ensure backend and backend/app in path
backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend"))
sys.path.insert(0, backend_path)
sys.path.insert(0, os.path.join(backend_path, "app"))

from app.scraper.mock_adapter import MockDirectoryAdapter
from app.scraper.rate_limiter import RateLimiter
from app.pipeline.validator import RecordValidator
from app.pipeline.normalizer import RecordNormalizer
from app.pipeline.deduplicator import RecordDeduplicator
from app.pipeline.quality import DataQualityScorer
from app.database.session import SessionLocal, init_db

async def run_benchmark(num_pages: int = 10, concurrency: int = 5, rate: float = 20.0):
    print("=" * 60)
    print(" Council of Architecture Extraction Pipeline Benchmark")
    print(f" Pages: {num_pages} | Concurrency: {concurrency} | Target Rate: {rate} req/s")
    print("=" * 60)

    tracemalloc.start()

    init_db()
    db = SessionLocal()
    deduplicator = RecordDeduplicator(db)

    rate_limiter = RateLimiter(requests_per_second=rate, max_concurrency=concurrency)
    adapter = MockDirectoryAdapter(rate_limiter=rate_limiter, simulated_delay=0.01)

    start_time = time.monotonic()
    total_records = 0
    valid_records = 0
    duplicate_records = 0
    failed_records = 0
    latencies = []

    for page in range(1, num_pages + 1):
        t0 = time.monotonic()
        html = await adapter.fetch_page(page)
        latencies.append(time.monotonic() - t0)

        raw_batch = adapter.parse_records(html)
        for raw in raw_batch:
            total_records += 1
            is_valid, _ = RecordValidator.validate(raw)
            if not is_valid:
                failed_records += 1
                continue
            normalized = RecordNormalizer.normalize(raw)
            if deduplicator.is_duplicate(normalized):
                duplicate_records += 1
                continue
            valid_records += 1

    total_duration = time.monotonic() - start_time
    current_mem, peak_mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    db.close()

    records_per_sec = total_records / total_duration if total_duration > 0 else 0
    pages_per_sec = num_pages / total_duration if total_duration > 0 else 0
    avg_latency_ms = (sum(latencies) / len(latencies) * 1000) if latencies else 0
    success_rate = (valid_records / total_records * 100) if total_records > 0 else 0
    duplicate_rate = (duplicate_records / total_records * 100) if total_records > 0 else 0

    print("\n--- BENCHMARK RESULTS ---")
    print(f"Total Duration:          {total_duration:.3f} s")
    print(f"Total Records Processed: {total_records}")
    print(f"Valid Records:           {valid_records}")
    print(f"Duplicate Records:       {duplicate_records}")
    print(f"Failed Records:          {failed_records}")
    print(f"Extraction Speed:        {records_per_sec:.1f} records/sec")
    print(f"Page Throughput:         {pages_per_sec:.1f} pages/sec")
    print(f"Average Page Latency:    {avg_latency_ms:.1f} ms")
    print(f"Pipeline Success Rate:   {success_rate:.1f} %")
    print(f"Duplicate Rate:          {duplicate_rate:.1f} %")
    print(f"Peak Memory Usage:       {peak_mem / (1024 * 1024):.2f} MB")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(run_benchmark())
