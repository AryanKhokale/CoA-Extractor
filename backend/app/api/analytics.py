from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.session import get_db
from schemas.analytics import AnalyticsSummary
from services.analytics_service import AnalyticsService

router = APIRouter(prefix="/analytics", tags=["Analytics & Data Quality"])

@router.get("", response_model=AnalyticsSummary)
def get_analytics(db: Session = Depends(get_db)):
    return AnalyticsService.get_summary(db)
