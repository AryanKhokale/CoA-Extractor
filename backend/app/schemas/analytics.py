from typing import List, Dict, Optional
from pydantic import BaseModel

class StateCount(BaseModel):
    state: str
    count: int

class CityCount(BaseModel):
    city: str
    count: int

class YearCount(BaseModel):
    year: int
    count: int

class StatusCount(BaseModel):
    status: str
    count: int

class ErrorCount(BaseModel):
    error_type: str
    count: int

class DataQualityMetrics(BaseModel):
    overall_score: float
    completeness: float
    validity: float
    uniqueness: float
    consistency: float
    total_audited: int
    description: Dict[str, str]

class AnalyticsSummary(BaseModel):
    total_records: int
    total_extracted: int
    total_successful: int
    total_failed: int
    total_duplicates: int
    active_jobs: int
    avg_speed_rec_sec: float
    data_quality_score: float
    states_distribution: List[StateCount]
    cities_distribution: List[CityCount]
    years_distribution: List[YearCount]
    status_distribution: List[StatusCount]
    errors_distribution: List[ErrorCount]
