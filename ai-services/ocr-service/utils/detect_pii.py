"""
detect_pii.py
-------------
Detects PII entities from OCR-extracted text using regex rules.

This module mirrors the NLP service output format so that
both services can be aggregated seamlessly in the backend.
"""

import re
from typing import List, Dict

# =========================
# Regex Patterns (OCR-safe)
# =========================
# OCR text is often noisy, so patterns are slightly tolerant
REGEX_PATTERNS = {
    "EMAIL": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
    "PHONE": r"(\+91[\-\s]?)?[6-9]\d{9}",
    "AADHAR": r"\d{4}\s?\d{4}\s?\d{4}",
    "PAN": r"[A-Z]{5}[0-9]{4}[A-Z]"
}

# =========================
# Severity Policy
# =========================
SEVERITY_MAP = {
    "AADHAR": "HIGH",
    "PAN": "HIGH",
    "PHONE": "MEDIUM",
    "EMAIL": "MEDIUM"
}

# =========================
# Confidence Policy
# =========================
# OCR is slightly less reliable than text regex
CONFIDENCE = {
    "OCR_REGEX": 0.90
}

# =========================
# Main Detection Function
# =========================
def detect_pii_from_text(text: str) -> Dict:
    """
    Detect PII from OCR-extracted text.

    Args:
        text (str): OCR extracted text

    Returns:
        {
            "has_violation": bool,
            "violation_count": int,
            "violations": list
        }
    """

    violations: List[Dict] = []

    if not text or not text.strip():
        return {
            "has_violation": False,
            "violation_count": 0,
            "violations": []
        }

    # Normalize OCR text
    normalized_text = text.replace("\n", " ").strip()

    # -------------------------
    # Regex Detection
    # -------------------------
    for pii_type, pattern in REGEX_PATTERNS.items():
        for match in re.finditer(pattern, normalized_text):
            violations.append({
                "type": pii_type,
                "text": match.group(),
                "start": match.start(),
                "end": match.end(),
                "source": "OCR_REGEX",
                "confidence": CONFIDENCE["OCR_REGEX"],
                "severity": SEVERITY_MAP.get(pii_type, "LOW")
            })

    # -------------------------
    # Deduplication
    # -------------------------
    unique = []
    seen = set()

    for v in violations:
        key = (v["type"], v["text"], v["start"], v["end"])
        if key not in seen:
            seen.add(key)
            unique.append(v)

    return {
        "has_violation": len(unique) > 0,
        "violation_count": len(unique),
        "violations": unique
    }


# =========================
# Local Test (Optional)
# =========================
if __name__ == "__main__":
    sample_text = """
    Name: Rahul Sharma
    Phone: 9876543210
    AADHAR: 1234 5678 9012
    Email: rahul.sharma@gmail.com
    """

    from pprint import pprint
    pprint(detect_pii_from_text(sample_text))
