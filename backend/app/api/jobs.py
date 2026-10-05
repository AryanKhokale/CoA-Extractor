import uuid
import json
import asyncio
from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from fastapi.responses import StreamingResponse
from sse_starlette.sse import EventSourceResponse
from sqlalchemy.orm import Session
from sqlalchemy import desc

from database.session import get_db
from models.job import ExtractionJob, JobStatus
from models.architect import Architect
from models.error import ExtractionError
from schemas.job import JobCreateRequest, JobRead
from schemas.architect import ArchitectListResponse
from services.job_manager import job_manager
from services.export_service import ExportService
from core.config import settings

router = APIRouter(prefix="/jobs", tags=["Extraction Jobs"])

@router.post("", response_model=JobRead)
async def create_job(
    request: JobCreateRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    # Enforce safe parameter maximums
    safe_concurrency = min(request.concurrency, settings.MAX_CONCURRENCY)
    safe_rate = min(request.requests_per_second, 5.0)
    
    # Generate unique ID
    job_id = f"job_{uuid.uuid4().hex[:10]}"
    
    # Mode selection
    mode = "mock" if (request.mode == "mock" or settings.USE_MOCK_DATA) else "live"

    job = ExtractionJob(
        id=job_id,
        status=JobStatus.PENDING.value,
        start_page=request.start_page,
        end_page=request.end_page,
        concurrency=safe_concurrency,
        requests_per_second=safe_rate,
        timeout_seconds=request.timeout_seconds,
        retry_count=request.retry_count,
        mode=mode,
        created_at=datetime.utcnow()
    )
    db.add(job)
    db.commit()
    db.refresh(job)

    # Launch async pipeline task
    await job_manager.start_job(job_id)

    return job

@router.get("", response_model=List[JobRead])
def list_jobs(
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    return db.query(ExtractionJob).order_by(desc(ExtractionJob.created_at)).limit(limit).all()

@router.get("/{job_id}", response_model=JobRead)
def get_job(job_id: str, db: Session = Depends(get_db)):
    job = db.query(ExtractionJob).filter(ExtractionJob.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@router.post("/{job_id}/cancel")
def cancel_job(job_id: str, db: Session = Depends(get_db)):
    job = db.query(ExtractionJob).filter(ExtractionJob.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    if job.status not in [JobStatus.PENDING.value, JobStatus.RUNNING.value]:
        return {"message": f"Job is already in status {job.status}"}

    success = job_manager.cancel_job(job_id)
    if not success:
        # If not active in memory, mark directly
        job.status = JobStatus.CANCELLED.value
        job.completed_at = datetime.utcnow()
        db.commit()

    return {"message": "Cancellation initiated", "job_id": job_id}

@router.post("/{job_id}/retry", response_model=JobRead)
async def retry_job(job_id: str, db: Session = Depends(get_db)):
    old_job = db.query(ExtractionJob).filter(ExtractionJob.id == job_id).first()
    if not old_job:
        raise HTTPException(status_code=404, detail="Job not found")

    new_id = f"job_{uuid.uuid4().hex[:10]}"
    retry_job = ExtractionJob(
        id=new_id,
        status=JobStatus.PENDING.value,
        start_page=old_job.start_page,
        end_page=old_job.end_page,
        concurrency=old_job.concurrency,
        requests_per_second=old_job.requests_per_second,
        timeout_seconds=old_job.timeout_seconds,
        retry_count=old_job.retry_count,
        mode=old_job.mode,
        created_at=datetime.utcnow()
    )
    db.add(retry_job)
    db.commit()
    db.refresh(retry_job)

    await job_manager.start_job(new_id)
    return retry_job

@router.get("/{job_id}/events")
async def stream_job_events(job_id: str):
    """
    Server-Sent Events endpoint streaming real-time job progress to the browser.
    """
    queue = job_manager.register_listener(job_id)

    async def event_generator():
        try:
            while True:
                # Wait for progress event
                try:
                    event = await asyncio.wait_for(queue.get(), timeout=20.0)
                    yield {
                        "event": "progress",
                        "data": json.dumps(event)
                    }
                    if event.get("status") in [JobStatus.COMPLETED.value, JobStatus.FAILED.value, JobStatus.CANCELLED.value]:
                        break
                except asyncio.TimeoutError:
                    # Keep-alive heartbeat ping
                    yield {
                        "event": "ping",
                        "data": json.dumps({"ping": True})
                    }
        finally:
            job_manager.unregister_listener(job_id, queue)

    return EventSourceResponse(event_generator())

@router.get("/{job_id}/records", response_model=ArchitectListResponse)
def get_job_records(
    job_id: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(25, ge=5, le=100),
    db: Session = Depends(get_db)
):
    q = db.query(Architect).filter(Architect.job_id == job_id)
    total = q.count()
    items = q.offset((page - 1) * page_size).limit(page_size).all()
    total_pages = max(1, (total + page_size - 1) // page_size)
    return ArchitectListResponse(
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
        items=items
    )

@router.get("/{job_id}/errors")
def get_job_errors(job_id: str, db: Session = Depends(get_db)):
    errors = db.query(ExtractionError).filter(ExtractionError.job_id == job_id).all()
    return errors

@router.get("/{job_id}/export/csv")
def export_job_csv(job_id: str, db: Session = Depends(get_db)):
    return StreamingResponse(
        ExportService.stream_csv(db, job_id=job_id),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=coa_records_{job_id}.csv"}
    )

@router.get("/{job_id}/export/json")
def export_job_json(job_id: str, db: Session = Depends(get_db)):
    return StreamingResponse(
        ExportService.stream_json(db, job_id=job_id),
        media_type="application/json",
        headers={"Content-Disposition": f"attachment; filename=coa_records_{job_id}.json"}
    )
