from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime
from database.session import Base

class ExtractionError(Base):
    __tablename__ = "extraction_errors"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    job_id = Column(String(50), index=True, nullable=False)
    page = Column(Integer, nullable=True)
    error_type = Column(String(50), index=True, nullable=False)  # TIMEOUT, RATE_LIMITED, PARSE_ERROR, HTTP_500, etc.
    error_message = Column(Text, nullable=False)
    record_identifier = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
