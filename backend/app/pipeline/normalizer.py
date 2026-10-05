import unicodedata
import re
from typing import Dict, Any, Optional

# Indian major cities to state mapping dictionary for automatic state normalization
CITY_TO_STATE = {
    "mumbai": "Maharashtra", "pune": "Maharashtra", "nagpur": "Maharashtra",
    "nashik": "Maharashtra", "aurangabad": "Maharashtra", "thane": "Maharashtra",
    "navi mumbai": "Maharashtra", "solapur": "Maharashtra", "kolhapur": "Maharashtra",
    "bengaluru": "Karnataka", "bangalore": "Karnataka", "mysore": "Karnataka",
    "mysuru": "Karnataka", "hubli": "Karnataka", "mangalore": "Karnataka",
    "mangaluru": "Karnataka", "belgaum": "Karnataka",
    "new delhi": "Delhi", "delhi": "Delhi", "ncr": "Delhi",
    "chennai": "Tamil Nadu", "madras": "Tamil Nadu", "coimbatore": "Tamil Nadu",
    "madurai": "Tamil Nadu", "tiruchirappalli": "Tamil Nadu", "salem": "Tamil Nadu",
    "hyderabad": "Telangana", "secunderabad": "Telangana", "warangal": "Telangana",
    "kolkata": "West Bengal", "calcutta": "West Bengal", "howrah": "West Bengal",
    "ahmedabad": "Gujarat", "surat": "Gujarat", "vadodara": "Gujarat",
    "rajkot": "Gujarat", "gandhinagar": "Gujarat",
    "jaipur": "Rajasthan", "jodhpur": "Rajasthan", "udaipur": "Rajasthan", "kota": "Rajasthan",
    "lucknow": "Uttar Pradesh", "noida": "Uttar Pradesh", "greater noida": "Uttar Pradesh",
    "ghaziabad": "Uttar Pradesh", "kanpur": "Uttar Pradesh", "agra": "Uttar Pradesh",
    "varanasi": "Uttar Pradesh", "prayagraj": "Uttar Pradesh", "allahabad": "Uttar Pradesh",
    "chandigarh": "Chandigarh",
    "bhopal": "Madhya Pradesh", "indore": "Madhya Pradesh", "gwalior": "Madhya Pradesh",
    "kochi": "Kerala", "cochin": "Kerala", "thiruvananthapuram": "Kerala", "trivandrum": "Kerala",
    "kozhikode": "Kerala", "calicut": "Kerala",
    "patna": "Bihar", "gaya": "Bihar",
    "ranchi": "Jharkhand", "jamshedpur": "Jharkhand",
    "bhubaneswar": "Odisha", "cuttack": "Odisha",
    "guwahati": "Assam", "silchar": "Assam",
    "dehradun": "Uttarakhand", "haridwar": "Uttarakhand",
    "shimla": "Himachal Pradesh", "dharamshala": "Himachal Pradesh",
    "panaji": "Goa", "margao": "Goa", "goa": "Goa",
    "visakhapatnam": "Andhra Pradesh", "vijayawada": "Andhra Pradesh", "guntur": "Andhra Pradesh"
}

class RecordNormalizer:
    """
    Normalizes whitespace, Unicode character sets, honorific casing,
    location references, and date structures.
    """

    @staticmethod
    def normalize_text(text: Optional[str]) -> str:
        if not text:
            return ""
        # 1. Unicode normalization (NFKC decomposes compatibility chars and re-composes standard canonical)
        normalized = unicodedata.normalize("NFKC", str(text))
        # 2. Replace non-breaking spaces and linebreaks with standard single space
        normalized = re.sub(r"[\r\n\t\xa0]+", " ", normalized)
        # 3. Collapse multiple spaces
        normalized = re.sub(r"\s+", " ", normalized).strip()
        return normalized

    @classmethod
    def normalize_name(cls, name: str) -> str:
        text = cls.normalize_text(name)
        # Title case while respecting honorifics
        words = text.split(" ")
        title_cased = []
        for w in words:
            wl = w.lower()
            if wl in ["ar.", "mr.", "ms.", "mrs.", "dr.", "prof."]:
                title_cased.append(wl.capitalize())
            elif "." in w:
                # E.g. N.T. or S.
                parts = [p.capitalize() for p in w.split(".") if p]
                title_cased.append(".".join(parts) + ".")
            else:
                title_cased.append(w.capitalize())
        return " ".join(title_cased)

    @classmethod
    def infer_state_from_city(cls, city: str, current_state: Optional[str] = None) -> Optional[str]:
        if current_state and current_state.strip():
            return cls.normalize_text(current_state).title()
        city_clean = cls.normalize_text(city).lower()
        return CITY_TO_STATE.get(city_clean, None)

    @classmethod
    def extract_registration_year(cls, reg_no: str, valid_up_to: Optional[str] = None) -> Optional[int]:
        # Extract from CA/YYYY/NNNNN
        match = re.search(r"CA\/(\d{4})\/", reg_no.upper())
        if match:
            try:
                year = int(match.group(1))
                if 1972 <= year <= 2030:
                    return year
            except ValueError:
                pass
        return None

    @classmethod
    def normalize(cls, record: Dict[str, Any]) -> Dict[str, Any]:
        """Produce clean, normalized representation of architect record."""
        reg_no = cls.normalize_text(record.get("registration_number", "")).upper()
        raw_name = record.get("name", "")
        name = cls.normalize_name(raw_name)
        
        city = cls.normalize_text(record.get("city", "")).title() or None
        state = record.get("state")
        state_inferred = cls.infer_state_from_city(city or "", state)
        
        valid_up_to = cls.normalize_text(record.get("valid_up_to", "")) or None
        reg_year = record.get("registration_year") or cls.extract_registration_year(reg_no, valid_up_to)
        
        # Determine status
        status = record.get("status") or "Active"
        if valid_up_to and "/" in valid_up_to:
            try:
                parts = valid_up_to.split("/")
                if len(parts) == 3:
                    v_year = int(parts[2])
                    if v_year < 2026:
                        status = "Inactive"
                    else:
                        status = "Active"
            except Exception:
                pass

        return {
            "registration_number": reg_no,
            "name": name,
            "normalized_name": name.lower(),
            "city": city,
            "state": state_inferred,
            "valid_up_to": valid_up_to,
            "registration_year": reg_year,
            "qualification": cls.normalize_text(record.get("qualification", "")) or None,
            "status": status,
            "address": cls.normalize_text(record.get("address", "")) or None,
            "raw_data": record.get("raw_data") or record
        }
