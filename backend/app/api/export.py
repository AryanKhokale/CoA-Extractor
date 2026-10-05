from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from database.session import get_db
from services.export_service import ExportService

router = APIRouter(prefix="/export", tags=["Exports"])

@router.get("/csv")
def export_all_csv(db: Session = Depends(get_db)):
    return StreamingResponse(
        ExportService.stream_csv(db),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=all_coa_architects.csv"}
    )

@router.get("/json")
def export_all_json(db: Session = Depends(get_db)):
    return StreamingResponse(
        ExportService.stream_json(db),
        media_type="application/json",
        headers={"Content-Disposition": "attachment; filename=all_coa_architects.json"}
    )
