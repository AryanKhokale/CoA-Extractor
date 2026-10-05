import os
import sys

# Ensure current app directory is on sys.path for robust resolution
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from database.session import init_db, SessionLocal
from api.health import router as health_router
from api.directory import router as directory_router
from api.jobs import router as jobs_router
from api.analytics import router as analytics_router
from api.export import router as export_router
from api.config import router as config_router
from models.architect import Architect
import json
import os

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("coa_extractor")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize DB schema
    logger.info("Initializing database schema...")
    init_db()

    # Pre-seed initial mock records if database is completely empty
    db = SessionLocal()
    try:
        count = db.query(Architect).count()
        if count == 0:
            mock_path = os.path.join(os.path.dirname(__file__), "..", "..", "mock_data", "architects.json")
            if os.path.exists(mock_path):
                logger.info("Pre-seeding initial CoA architect records...")
                with open(mock_path, "r", encoding="utf-8") as f:
                    records = json.load(f)
                
                seen_regs = set()
                architect_objects = []
                for r in records[:50]:  # Seed first 50 records
                    reg = r.get("registration_number", "").upper()
                    if reg in seen_regs:
                        continue
                    seen_regs.add(reg)
                    arch = Architect(
                        registration_number=reg,
                        name=r.get("name"),
                        normalized_name=r.get("name", "").lower(),
                        city=r.get("city"),
                        state=r.get("state"),
                        valid_up_to=r.get("valid_up_to"),
                        registration_year=r.get("registration_year"),
                        qualification=r.get("qualification"),
                        status=r.get("status", "Active"),
                        address=r.get("address"),
                        job_id="seed_initial",
                        raw_data=r.get("raw_data")
                    )
                    architect_objects.append(arch)
                db.bulk_save_objects(architect_objects)
                db.commit()
                logger.info(f"Seeded {len(architect_objects)} initial records.")
    except Exception as e:
        logger.error(f"Error seeding database: {e}")
    finally:
        db.close()

    yield
    logger.info("Application shutdown completed.")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="High-Speed Council of Architecture (CoA) Public Directory Extraction & Analytics Platform",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS
origins = settings.CORS_ORIGINS if isinstance(settings.CORS_ORIGINS, list) else ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Routers
app.include_router(health_router, prefix=settings.API_V1_PREFIX)
app.include_router(directory_router, prefix=settings.API_V1_PREFIX)
app.include_router(jobs_router, prefix=settings.API_V1_PREFIX)
app.include_router(analytics_router, prefix=settings.API_V1_PREFIX)
app.include_router(export_router, prefix=settings.API_V1_PREFIX)
app.include_router(config_router, prefix=settings.API_V1_PREFIX)

@app.get("/")
def root():
    return {
        "message": "Council of Architecture Data Extraction API is running",
        "documentation": "/docs",
        "health": f"{settings.API_V1_PREFIX}/health"
    }
