from fastapi import APIRouter
from core.config import settings

router = APIRouter(tags=["Health"])

@router.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "coa-directory-extractor",
        "version": settings.VERSION
    }
