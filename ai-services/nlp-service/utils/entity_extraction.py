"""
entity_extraction.py
--------------------
Hybrid PII detection using:
1. spaCy NER (semantic detection)
2. Regex rules (deterministic detection)

This file is the CORE intelligence of the entire system.
"""

import re
import spacy
from typing import List, Dict

# =========================
# Load spaCy Model
# =========================
# Lightweight & fast (good for Lambda / App Runner)
nlp = spacy.load("en_core_web_sm")

# =========================
# Regex Patterns (India-Focused)
# =========================
REGEX_PATTERNS = {
    "EMAIL": r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b",
    "PHONE": r"\b(\+91[\-\s]?)?[6-9]\d{9}\b",
    "AADHAR": r"\b\d{4}\s\d{4}\s\d{4}\b",
    "PAN": r"\b[A-Z]{5}[0-9]{4}[A-Z]\b"
}

# =========================
# Severity Policy
# =========================
SEVERITY_MAP = {
    "AADHAR": "HIGH",
    "PAN": "HIGH",
    "PHONE": "MEDIUM",
    "EMAIL": "MEDIUM",
    "LOCATION": "HIGH",
}

# =========================
# Confidence Scores
# =========================
CONFIDENCE = {
    "NER": 0.85,
    "REGEX": 0.95
}

# =========================
# Main Extraction Function
# =========================
def extract_pii(text: str) -> Dict:
    """
    Analyze text and return structured PII violations

    Returns:
    {
        "has_violation": bool,
        "violations": [ {...}, {...} ]
    }
    """

    violations: List[Dict] = []

    # -------------------------
    # 1. spaCy NER Detection
    # -------------------------
    doc = nlp(text)

    for ent in doc.ents:
        # Locations are sensitive in privacy context
        if ent.label_ in ["GPE", "LOC"]:
            violations.append({
                "type": "LOCATION",
                "text": ent.text,
                "start": ent.start_char,
                "end": ent.end_char,
                "source": "NER",
                "confidence": CONFIDENCE["NER"],
                "severity": SEVERITY_MAP["LOCATION"]
            })

    # -------------------------
    # 2. Regex-Based Detection
    # -------------------------
    for pii_type, pattern in REGEX_PATTERNS.items():
        for match in re.finditer(pattern, text):
            violations.append({
                "type": pii_type,
                "text": match.group(),
                "start": match.start(),
                "end": match.end(),
                "source": "REGEX",
                "confidence": CONFIDENCE["REGEX"],
                "severity": SEVERITY_MAP.get(pii_type, "LOW")
            })

    # -------------------------
    # 3. Deduplication
    # -------------------------
    unique = []
    seen = set()

    for v in violations:
        key = (v["type"], v["text"], v["start"], v["end"])
        if key not in seen:
            seen.add(key)
            unique.append(v)

    # -------------------------
    # 4. Final Response
    # -------------------------
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
    My phone number is 9876543210.
    My PAN is ABCDE1234F.
    I live in Pune, Maharashtra.
    Email me at test.user@gmail.com
    """

    result = extract_pii(sample_text)
    from pprint import pprint
    pprint(result)
