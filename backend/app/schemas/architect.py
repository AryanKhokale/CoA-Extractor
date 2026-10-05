from typing import Optional, Dict, Any, List
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

class ArchitectBase(BaseModel):
    registration_number: str = Field(..., description="CoA Registration Code (e.g. CA/1975/00005)")
    name: str = Field(..., description="Full name of architect")
    city: Optional[str] = Field(None, description="City of practice")
    state: Optional[str] = Field(None, description="State / Union Territory")
    valid_up_to: Optional[str] = Field(None, description="Validity string DD/MM/YYYY")
    registration_year: Optional[int] = Field(None, description="Registration year")
    qualification: Optional[str] = Field(None, description="Degree or diploma qualification")
    status: Optional[str] = Field("Active", description="Registration standing: Active, Inactive, Defaulter")
    address: Optional[str] = Field(None, description="Office or residential address")

class ArchitectCreate(ArchitectBase):
    normalized_name: Optional[str] = None
    job_id: Optional[str] = None
    raw_data: Optional[Dict[str, Any]] = None

class ArchitectRead(ArchitectBase):
    id: int
    normalized_name: str
    job_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ArchitectListResponse(BaseModel):
    total: int
    page: int
    page_size: int
    total_pages: int
    items: List[ArchitectRead]
