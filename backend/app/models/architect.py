from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from database.session import Base

class Architect(Base):
    __tablename__ = "architects"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    registration_number = Column(String(50), unique=True, index=True, nullable=False)
    name = Column(String(255), index=True, nullable=False)
    normalized_name = Column(String(255), index=True, nullable=False)
    
    city = Column(String(100), index=True, nullable=True)
    state = Column(String(100), index=True, nullable=True)
    valid_up_to = Column(String(30), nullable=True)
    registration_year = Column(Integer, index=True, nullable=True)
    
    qualification = Column(String(255), nullable=True)
    status = Column(String(50), default="Active", index=True)
    address = Column(Text, nullable=True)
    
    job_id = Column(String(50), index=True, nullable=True)
    raw_data = Column(JSON, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
