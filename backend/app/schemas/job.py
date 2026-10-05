from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from models.job import JobStatus

class JobCreateRequest(BaseModel):
    start_page: int = Field(1, ge=1, description="First page to extract")
    end_page: int = Field(5, ge=1, le=1000, description="Last page to extract")
    concurrency: int = Field(5, ge=1, le=10, description="Bounded concurrent workers")
    requests_per_second: float = Field(2.0, ge=0.5, le=5.0, description="Rate limit (req/sec)")
    timeout_seconds: int = Field(30, ge=5, le=60, description="Timeout per request in seconds")
    retry_count: int = Field(3, ge=1, le=5, description="Maximum retries for transient errors")
    mode: str = Field("live", description="Extraction mode: 'live' or 'mock'")

class JobRead(BaseModel):
    id: str
    status: JobStatus
    total_target: int
    processed_records: int
    successful_records: int
    failed_records: int
    duplicate_records: int
    start_page: int
    end_page: int
    current_page: int
    concurrency: int
    requests_per_second: float
    timeout_seconds: int
    retry_count: int
    mode: str
    error_message: Optional[str] = None
    speed_records_per_sec: float
    data_quality_score: float
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class JobProgressEvent(BaseModel):
    job_id: str
    status: JobStatus
    total_target: int
    processed_records: int
    successful_records: int
    failed_records: int
    duplicate_records: int
    current_page: int
    progress_percentage: float
    speed_records_per_sec: float
    elapsed_seconds: float
    estimated_remaining_seconds: Optional[float] = None
    error_message: Optional[str] = None
    timestamp: datetime
