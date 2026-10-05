from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from models.architect import Architect
from models.job import ExtractionJob, JobStatus
from models.error import ExtractionError
from schemas.analytics import AnalyticsSummary, StateCount, CityCount, YearCount, StatusCount, ErrorCount
from pipeline.quality import DataQualityScorer

class AnalyticsService:
    @staticmethod
    def get_summary(db: Session) -> AnalyticsSummary:
        total_records = db.query(Architect).count()
        
        # Aggregate job stats
        job_totals = db.query(
            func.coalesce(func.sum(ExtractionJob.processed_records), 0),
            func.coalesce(func.sum(ExtractionJob.successful_records), 0),
            func.coalesce(func.sum(ExtractionJob.failed_records), 0),
            func.coalesce(func.sum(ExtractionJob.duplicate_records), 0),
            func.coalesce(func.avg(ExtractionJob.speed_records_per_sec), 0.0)
        ).first()

        total_extracted = int(job_totals[0])
        total_successful = int(job_totals[1])
        total_failed = int(job_totals[2])
        total_duplicates = int(job_totals[3])
        avg_speed = round(float(job_totals[4]), 1)

        active_jobs = db.query(ExtractionJob).filter(ExtractionJob.status == JobStatus.RUNNING.value).count()

        # State distribution
        state_rows = db.query(
            Architect.state,
            func.count(Architect.id).label("count")
        ).filter(Architect.state.isnot(None))\
         .group_by(Architect.state)\
         .order_by(desc("count"))\
         .limit(15).all()

        states_distribution = [StateCount(state=s or "Unknown", count=c) for s, c in state_rows]

        # City distribution
        city_rows = db.query(
            Architect.city,
            func.count(Architect.id).label("count")
        ).filter(Architect.city.isnot(None))\
         .group_by(Architect.city)\
         .order_by(desc("count"))\
         .limit(10).all()

        cities_distribution = [CityCount(city=c or "Unknown", count=cnt) for c, cnt in city_rows]

        # Year distribution
        year_rows = db.query(
            Architect.registration_year,
            func.count(Architect.id).label("count")
        ).filter(Architect.registration_year.isnot(None))\
         .group_by(Architect.registration_year)\
         .order_by(Architect.registration_year.asc())\
         .all()

        years_distribution = [YearCount(year=y, count=c) for y, c in year_rows if y and y >= 1975]

        # Status distribution
        status_rows = db.query(
            Architect.status,
            func.count(Architect.id).label("count")
        ).group_by(Architect.status).all()

        status_distribution = [StatusCount(status=s or "Active", count=c) for s, c in status_rows]

        # Error distribution
        error_rows = db.query(
            ExtractionError.error_type,
            func.count(ExtractionError.id).label("count")
        ).group_by(ExtractionError.error_type).all()

        errors_distribution = [ErrorCount(error_type=e, count=c) for e, c in error_rows]

        # Calculate sample data quality score
        sample_records = db.query(Architect).limit(300).all()
        sample_dicts = [
            {
                "registration_number": a.registration_number,
                "name": a.name,
                "city": a.city,
                "state": a.state,
                "valid_up_to": a.valid_up_to,
                "registration_year": a.registration_year
            }
            for a in sample_records
        ]
        quality_res = DataQualityScorer.score_dataset(sample_dicts, total_duplicates)

        return AnalyticsSummary(
            total_records=total_records,
            total_extracted=total_extracted,
            total_successful=total_successful,
            total_failed=total_failed,
            total_duplicates=total_duplicates,
            active_jobs=active_jobs,
            avg_speed_rec_sec=avg_speed,
            data_quality_score=quality_res["overall_score"],
            states_distribution=states_distribution,
            cities_distribution=cities_distribution,
            years_distribution=years_distribution,
            status_distribution=status_distribution,
            errors_distribution=errors_distribution
        )
