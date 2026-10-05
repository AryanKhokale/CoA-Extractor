import csv
import io
import json
from typing import AsyncGenerator
from sqlalchemy.orm import Session
from models.architect import Architect

class ExportService:
    @staticmethod
    def stream_csv(db: Session, job_id: str = None) -> AsyncGenerator[str, None]:
        output = io.StringIO()
        writer = csv.writer(output)

        # Header
        headers = [
            "Registration Number", "Name", "City", "State",
            "Valid Up To", "Registration Year", "Qualification", "Status", "Address"
        ]
        writer.writerow(headers)
        yield output.getvalue()
        output.seek(0)
        output.truncate(0)

        # Query batch by batch using yield_per
        query = db.query(Architect)
        if job_id:
            query = query.filter(Architect.job_id == job_id)

        for arch in query.yield_per(500):
            writer.writerow([
                arch.registration_number,
                arch.name,
                arch.city or "",
                arch.state or "",
                arch.valid_up_to or "",
                arch.registration_year or "",
                arch.qualification or "",
                arch.status or "",
                arch.address or ""
            ])
            yield output.getvalue()
            output.seek(0)
            output.truncate(0)

    @staticmethod
    def stream_json(db: Session, job_id: str = None) -> AsyncGenerator[str, None]:
        yield "[\n"
        query = db.query(Architect)
        if job_id:
            query = query.filter(Architect.job_id == job_id)

        first = True
        for arch in query.yield_per(500):
            record = {
                "registration_number": arch.registration_number,
                "name": arch.name,
                "city": arch.city,
                "state": arch.state,
                "valid_up_to": arch.valid_up_to,
                "registration_year": arch.registration_year,
                "qualification": arch.qualification,
                "status": arch.status,
                "address": arch.address
            }
            prefix = "" if first else ",\n"
            first = False
            yield prefix + json.dumps(record, ensure_ascii=False)

        yield "\n]"
