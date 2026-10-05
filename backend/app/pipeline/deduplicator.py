from typing import Set, Dict, Any, Tuple
from sqlalchemy.orm import Session
from models.architect import Architect

class RecordDeduplicator:
    """
    High-speed duplicate detection engine.
    Uses primary stable identifier (registration_number) with composite fallback.
    """
    def __init__(self, db: Session):
        self.db = db
        # Pre-populate known registration numbers into a set for fast O(1) checks
        self.seen_reg_numbers: Set[str] = set()
        self.seen_composite_keys: Set[Tuple[str, str]] = set()

    def load_existing_keys(self):
        """Warm up in-memory index from database."""
        records = self.db.query(Architect.registration_number, Architect.normalized_name, Architect.city).all()
        for reg_no, norm_name, city in records:
            if reg_no:
                self.seen_reg_numbers.add(reg_no.upper().strip())
            if norm_name and city:
                self.seen_composite_keys.add((norm_name.strip().lower(), (city or "").strip().lower()))

    def is_duplicate(self, record: Dict[str, Any]) -> bool:
        """
        Check if record already exists. If not, marks it as seen and returns False.
        If duplicate, returns True.
        """
        reg_no = (record.get("registration_number") or "").upper().strip()
        norm_name = (record.get("normalized_name") or record.get("name") or "").lower().strip()
        city = (record.get("city") or "").lower().strip()

        # Primary check: registration number
        if reg_no and reg_no in self.seen_reg_numbers:
            return True

        # Secondary composite fallback check: (normalized_name, city)
        composite_key = (norm_name, city)
        if norm_name and city and composite_key in self.seen_composite_keys:
            return True

        # Register key
        if reg_no:
            self.seen_reg_numbers.add(reg_no)
        if norm_name and city:
            self.seen_composite_keys.add(composite_key)

        return False
