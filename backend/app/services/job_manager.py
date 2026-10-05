import asyncio
import time
import logging
from datetime import datetime
from typing import Dict, Optional, AsyncGenerator
from sqlalchemy.orm import Session
from database.session import SessionLocal
from models.job import ExtractionJob, JobStatus
from models.architect import Architect
from models.error import ExtractionError
from scraper.rate_limiter import RateLimiter
from scraper.coa_adapter import CoADirectoryAdapter
from scraper.mock_adapter import MockDirectoryAdapter
from pipeline.validator import RecordValidator
from pipeline.normalizer import RecordNormalizer
from pipeline.deduplicator import RecordDeduplicator
from pipeline.quality import DataQualityScorer
from schemas.job import JobProgressEvent

logger = logging.getLogger(__name__)

class JobManager:
    """
    Central Extraction Engine and Job Orchestrator.
    Manages background tasks, bounded concurrency, streaming event queues,
    cancellation tokens, and batch database transactions.
    """
    def __init__(self):
        self.active_tasks: Dict[str, asyncio.Task] = {}
        self.cancellation_events: Dict[str, asyncio.Event] = {}
        self.event_queues: Dict[str, list[asyncio.Queue]] = {}

    def register_listener(self, job_id: str) -> asyncio.Queue:
        q: asyncio.Queue = asyncio.Queue()
        if job_id not in self.event_queues:
            self.event_queues[job_id] = []
        self.event_queues[job_id].append(q)
        return q

    def unregister_listener(self, job_id: str, q: asyncio.Queue):
        if job_id in self.event_queues and q in self.event_queues[job_id]:
            self.event_queues[job_id].remove(q)
            if not self.event_queues[job_id]:
                del self.event_queues[job_id]

    async def broadcast_event(self, job_id: str, event_data: dict):
        if job_id in self.event_queues:
            for q in list(self.event_queues[job_id]):
                try:
                    q.put_nowait(event_data)
                except asyncio.QueueFull:
                    pass

    def cancel_job(self, job_id: str) -> bool:
        if job_id in self.cancellation_events:
            self.cancellation_events[job_id].set()
            logger.info(f"Cancellation requested for job {job_id}")
            return True
        return False

    async def start_job(self, job_id: str):
        cancel_event = asyncio.Event()
        self.cancellation_events[job_id] = cancel_event
        task = asyncio.create_task(self._run_job(job_id, cancel_event))
        self.active_tasks[job_id] = task

    async def _run_job(self, job_id: str, cancel_event: asyncio.Event):
        db: Session = SessionLocal()
        start_time = time.monotonic()
        
        try:
            job = db.query(ExtractionJob).filter(ExtractionJob.id == job_id).first()
            if not job:
                logger.error(f"Job {job_id} not found in database")
                return

            job.status = JobStatus.RUNNING.value
            job.started_at = datetime.utcnow()
            total_pages = job.end_page - job.start_page + 1
            job.total_target = total_pages * 50  # 50 records per page
            db.commit()

            # Initialize Rate Limiter & Adapter
            rate_limiter = RateLimiter(
                requests_per_second=job.requests_per_second,
                max_concurrency=job.concurrency
            )

            if job.mode == "mock":
                adapter = MockDirectoryAdapter(rate_limiter=rate_limiter)
            else:
                adapter = CoADirectoryAdapter(
                    rate_limiter=rate_limiter,
                    timeout=job.timeout_seconds,
                    max_retries=job.retry_count
                )

            deduplicator = RecordDeduplicator(db)
            deduplicator.load_existing_keys()

            all_valid_records = []
            
            for current_page in range(job.start_page, job.end_page + 1):
                # Check cancellation token
                if cancel_event.is_set():
                    job.status = JobStatus.CANCELLED.value
                    job.completed_at = datetime.utcnow()
                    db.commit()
                    logger.info(f"Job {job_id} successfully cancelled at page {current_page}")
                    await self._emit_progress(job, start_time, "Job cancelled by user request")
                    break

                job.current_page = current_page
                
                # Fetch page
                try:
                    html_content = await adapter.fetch_page(current_page)
                    raw_records = adapter.parse_records(html_content)
                except Exception as exc:
                    err_msg = str(exc)
                    logger.error(f"Failed to fetch/parse page {current_page}: {err_msg}")
                    job.failed_records += 50
                    err = ExtractionError(
                        job_id=job_id,
                        page=current_page,
                        error_type="FETCH_ERROR",
                        error_message=err_msg
                    )
                    db.add(err)
                    db.commit()
                    await self._emit_progress(job, start_time, err_msg)
                    continue

                batch_to_insert = []
                for raw in raw_records:
                    job.processed_records += 1
                    
                    # 1. Validate
                    is_valid, reason = RecordValidator.validate(raw)
                    if not is_valid:
                        job.failed_records += 1
                        err = ExtractionError(
                            job_id=job_id,
                            page=current_page,
                            error_type="VALIDATION_ERROR",
                            error_message=reason or "Validation failed",
                            record_identifier=raw.get("registration_number")
                        )
                        db.add(err)
                        continue

                    # 2. Normalize
                    normalized = RecordNormalizer.normalize(raw)

                    # 3. Deduplicate
                    if deduplicator.is_duplicate(normalized):
                        job.duplicate_records += 1
                        continue

                    # 4. Prepare for Storage
                    arch = Architect(
                        registration_number=normalized["registration_number"],
                        name=normalized["name"],
                        normalized_name=normalized["normalized_name"],
                        city=normalized["city"],
                        state=normalized["state"],
                        valid_up_to=normalized["valid_up_to"],
                        registration_year=normalized["registration_year"],
                        qualification=normalized["qualification"],
                        status=normalized["status"],
                        address=normalized["address"],
                        job_id=job_id,
                        raw_data=normalized["raw_data"]
                    )
                    batch_to_insert.append(arch)
                    all_valid_records.append(normalized)
                    job.successful_records += 1

                # Persist batch and release memory
                if batch_to_insert:
                    db.bulk_save_objects(batch_to_insert)
                db.commit()

                # Update speed and progress
                elapsed = max(0.1, time.monotonic() - start_time)
                job.speed_records_per_sec = round(job.processed_records / elapsed, 1)
                db.commit()

                await self._emit_progress(job, start_time)

            # Finalize completion if not cancelled
            if not cancel_event.is_set():
                job.status = JobStatus.COMPLETED.value
                job.completed_at = datetime.utcnow()
                elapsed = max(0.1, time.monotonic() - start_time)
                job.speed_records_per_sec = round(job.processed_records / elapsed, 1)

                # Calculate Data Quality Score
                quality_report = DataQualityScorer.score_dataset(all_valid_records, job.duplicate_records)
                job.data_quality_score = quality_report["overall_score"]
                db.commit()

                await self._emit_progress(job, start_time)
                logger.info(f"Job {job_id} completed. Extracted: {job.successful_records}, Quality: {job.data_quality_score}%")

            await adapter.close()

        except Exception as exc:
            logger.exception(f"Unhandled error in job {job_id}: {exc}")
            job = db.query(ExtractionJob).filter(ExtractionJob.id == job_id).first()
            if job:
                job.status = JobStatus.FAILED.value
                job.error_message = str(exc)
                job.completed_at = datetime.utcnow()
                db.commit()
                await self._emit_progress(job, start_time, str(exc))

        finally:
            db.close()
            self.active_tasks.pop(job_id, None)
            self.cancellation_events.pop(job_id, None)

    async def _emit_progress(self, job: ExtractionJob, start_time: float, error_msg: Optional[str] = None):
        elapsed = max(0.1, time.monotonic() - start_time)
        speed = round(job.processed_records / elapsed, 1)
        total = max(1, job.total_target)
        pct = min(100.0, round((job.processed_records / total) * 100.0, 1))
        
        remaining_seconds = None
        if speed > 0 and job.processed_records < total:
            remaining_seconds = round((total - job.processed_records) / speed, 1)

        event = {
            "job_id": job.id,
            "status": job.status,
            "total_target": job.total_target,
            "processed_records": job.processed_records,
            "successful_records": job.successful_records,
            "failed_records": job.failed_records,
            "duplicate_records": job.duplicate_records,
            "current_page": job.current_page,
            "progress_percentage": pct,
            "speed_records_per_sec": speed,
            "elapsed_seconds": round(elapsed, 1),
            "estimated_remaining_seconds": remaining_seconds,
            "error_message": error_msg or job.error_message,
            "timestamp": datetime.utcnow().isoformat()
        }
        await self.broadcast_event(job.id, event)

# Global singleton
job_manager = JobManager()
