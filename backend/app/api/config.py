from fastapi import APIRouter
from core.config import settings

router = APIRouter(prefix="/config", tags=["System Configuration"])

@router.get("")
def get_config():
    return {
        "project_name": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "coa_base_url": settings.COA_BASE_URL,
        "max_concurrency": settings.MAX_CONCURRENCY,
        "default_requests_per_second": settings.REQUESTS_PER_SECOND,
        "default_timeout_seconds": settings.REQUEST_TIMEOUT,
        "default_retries": settings.MAX_RETRIES,
        "use_mock_data": settings.USE_MOCK_DATA,
        "status": "online"
    }
