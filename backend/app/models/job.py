import enum
from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, DateTime, Text, Enum
from database.session import Base

class JobStatus(str, enum.Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"

class ExtractionJob(Base):
    __tablename__ = "extraction_jobs"
    __table_args__ = {"extend_existing": True}

    id = Column(String(50), primary_key=True, index=True)
    status = Column(String(20), default=JobStatus.PENDING.value, index=True)
    
    total_target = Column(Integer, default=0)
    processed_records = Column(Integer, default=0)
    successful_records = Column(Integer, default=0)
    failed_records = Column(Integer, default=0)
    duplicate_records = Column(Integer, default=0)
    
    start_page = Column(Integer, default=1)
    end_page = Column(Integer, default=10)
    current_page = Column(Integer, default=1)
    
    concurrency = Column(Integer, default=5)
    requests_per_second = Column(Float, default=2.0)
    timeout_seconds = Column(Integer, default=30)
    retry_count = Column(Integer, default=3)
    
    mode = Column(String(20), default="live") # "live" or "mock"
    error_message = Column(Text, nullable=True)
    
    speed_records_per_sec = Column(Float, default=0.0)
    data_quality_score = Column(Float, default=0.0)
    
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
