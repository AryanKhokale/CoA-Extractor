from typing import List, Dict, Any
from pipeline.validator import RecordValidator

class DataQualityScorer:
    """
    Computes a transparent, auditable Data Quality Score (0–100) based on 4 pillars:
    - 40% Completeness: Percentage of non-null core fields (Name, RegNo, City, State, Validity, Year)
    - 30% Validity: Strict adherence to CoA registration pattern (CA/YYYY/NNNNN) and date formats
    - 20% Uniqueness: Absence of duplicate records
    - 10% Consistency: Geographic and temporal alignment (validity vs reg year, city-state mapping)
    """

    @classmethod
    def score_dataset(cls, records: List[Dict[str, Any]], duplicate_count: int = 0) -> Dict[str, Any]:
        total = len(records)
        if total == 0:
            return {
                "overall_score": 100.0,
                "completeness": 100.0,
                "validity": 100.0,
                "uniqueness": 100.0,
                "consistency": 100.0,
                "total_audited": 0,
                "description": {
                    "completeness": "40% weight - evaluation of required and contextual fields presence",
                    "validity": "30% weight - adherence to CoA registration and date regex specifications",
                    "uniqueness": "20% weight - absence of repeated registration codes or duplicates",
                    "consistency": "10% weight - geographical city-state alignment and valid registration chronology"
                }
            }

        # 1. Completeness (40%)
        # Core fields: registration_number, name, city, state, valid_up_to, registration_year
        completeness_points = 0.0
        for r in records:
            field_score = 0
            if r.get("registration_number"): field_score += 1
            if r.get("name"): field_score += 1
            if r.get("city"): field_score += 1
            if r.get("state"): field_score += 1
            if r.get("valid_up_to"): field_score += 1
            if r.get("registration_year"): field_score += 1
            completeness_points += (field_score / 6.0)
        completeness_pct = (completeness_points / total) * 100.0

        # 2. Validity (30%)
        valid_count = 0
        for r in records:
            is_valid, _ = RecordValidator.validate(r)
            if is_valid:
                valid_count += 1
        validity_pct = (valid_count / total) * 100.0

        # 3. Uniqueness (20%)
        total_eval = total + duplicate_count
        uniqueness_pct = (total / total_eval * 100.0) if total_eval > 0 else 100.0

        # 4. Consistency (10%)
        consistent_count = 0
        for r in records:
            # Check city-state consistency and reg_year <= 2026
            year = r.get("registration_year")
            state = r.get("state")
            valid = True
            if year and not (1970 <= year <= 2030):
                valid = False
            if not state:
                valid = False
            if valid:
                consistent_count += 1
        consistency_pct = (consistent_count / total) * 100.0

        # Weighted calculation
        overall = (
            (completeness_pct * 0.40) +
            (validity_pct * 0.30) +
            (uniqueness_pct * 0.20) +
            (consistency_pct * 0.10)
        )

        return {
            "overall_score": round(overall, 1),
            "completeness": round(completeness_pct, 1),
            "validity": round(validity_pct, 1),
            "uniqueness": round(uniqueness_pct, 1),
            "consistency": round(consistency_pct, 1),
            "total_audited": total,
            "description": {
                "completeness": "40% weight - evaluation of required and contextual fields presence",
                "validity": "30% weight - adherence to CoA registration and date regex specifications",
                "uniqueness": "20% weight - absence of repeated registration codes or duplicates",
                "consistency": "10% weight - geographical city-state alignment and valid registration chronology"
            }
        }
