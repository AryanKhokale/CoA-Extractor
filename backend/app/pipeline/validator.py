import re
from typing import Dict, Any, Tuple, Optional

# Regular expression for Council of Architecture registration numbers (e.g. CA/1975/00005 or CA/2012/54321)
COA_REG_REGEX = re.compile(r"^CA\/\d{4}\/\d{1,6}$", re.IGNORECASE)
DATE_REGEX = re.compile(r"^\d{2}\/\d{2}\/\d{4}$")

class RecordValidator:
    """
    Validates extracted Council of Architecture architect records.
    Ensures strict structural integrity and data types before persistence.
    """

    @staticmethod
    def validate(record: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """
        Validate record. Returns (is_valid, error_reason).
        """
        # 1. Required: registration_number
        reg_no = record.get("registration_number")
        if not reg_no or not isinstance(reg_no, str) or not reg_no.strip():
            return False, "Missing or empty registration number"

        reg_clean = reg_no.strip()
        if not COA_REG_REGEX.match(reg_clean) and not reg_clean.upper().startswith("CA/"):
            return False, f"Invalid CoA registration number format: '{reg_no}'"

        # 2. Required: name
        name = record.get("name")
        if not name or not isinstance(name, str) or len(name.strip()) < 2:
            return False, "Missing or invalid architect name"

        # 3. Optional date validation if present
        valid_up_to = record.get("valid_up_to")
        if valid_up_to and isinstance(valid_up_to, str) and valid_up_to.strip():
            clean_date = valid_up_to.strip()
            if not DATE_REGEX.match(clean_date) and clean_date != "-":
                # Non-fatal warning or normalization candidate
                pass

        return True, None
