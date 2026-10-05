from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, desc, asc
from database.session import get_db
from models.architect import Architect
from schemas.architect import ArchitectListResponse, ArchitectRead

router = APIRouter(prefix="/directory", tags=["Directory Explorer"])

@router.get("/architects", response_model=ArchitectListResponse)
def list_architects(
    query: Optional[str] = Query(None, description="Search query matching Name or Registration Number"),
    state: Optional[str] = Query(None, description="Filter by State"),
    city: Optional[str] = Query(None, description="Filter by City"),
    status: Optional[str] = Query(None, description="Filter by Status (Active, Inactive, Defaulter)"),
    sort_by: str = Query("registration_number", description="Field to sort by"),
    sort_order: str = Query("asc", description="'asc' or 'desc'"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(25, ge=5, le=100, description="Items per page"),
    db: Session = Depends(get_db)
):
    q = db.query(Architect)

    if query and query.strip():
        search_term = f"%{query.strip()}%"
        q = q.filter(
            or_(
                Architect.name.ilike(search_term),
                Architect.registration_number.ilike(search_term),
                Architect.city.ilike(search_term)
            )
        )

    if state and state.strip() and state != "All":
        q = q.filter(Architect.state.ilike(f"%{state.strip()}%"))

    if city and city.strip() and city != "All":
        q = q.filter(Architect.city.ilike(f"%{city.strip()}%"))

    if status and status.strip() and status != "All":
        q = q.filter(Architect.status == status.strip())

    total = q.count()

    # Sorting
    sort_column = getattr(Architect, sort_by, Architect.registration_number)
    if sort_order.lower() == "desc":
        q = q.order_by(desc(sort_column))
    else:
        q = q.order_by(asc(sort_column))

    items = q.offset((page - 1) * page_size).limit(page_size).all()
    total_pages = max(1, (total + page_size - 1) // page_size)

    return ArchitectListResponse(
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
        items=items
    )

@router.get("/search")
def search_directory(
    q: str = Query(..., min_length=2, description="Search query"),
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    term = f"%{q.strip()}%"
    results = db.query(Architect).filter(
        or_(
            Architect.name.ilike(term),
            Architect.registration_number.ilike(term)
        )
    ).limit(limit).all()
    return results

@router.get("/filters")
def get_filters(db: Session = Depends(get_db)):
    """Returns available distinct states, cities, and statuses for UI filter dropdowns."""
    states = [s[0] for s in db.query(Architect.state).filter(Architect.state.isnot(None)).distinct().order_by(Architect.state).all() if s[0]]
    cities = [c[0] for c in db.query(Architect.city).filter(Architect.city.isnot(None)).distinct().order_by(Architect.city).limit(50).all() if c[0]]
    statuses = [st[0] for st in db.query(Architect.status).distinct().all() if st[0]]
    return {
        "states": sorted(list(set(states))),
        "cities": sorted(list(set(cities))),
        "statuses": sorted(list(set(statuses)))
    }
