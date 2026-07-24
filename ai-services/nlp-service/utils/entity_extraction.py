import re
import time
from typing import List, Dict
from utils.preprocess import preprocess_for_ner
from utils.response_formatter import format_detection_response
from utils.llm_extraction import extract_pii_with_llm

REGEX_PATTERNS = {
    "EMAIL": r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b",
    "INDIAN_PHONE": r"\b(\+91[\-\s]?)?[6-9]\d{9}\b",
    "AADHAR": r"\b\d{4}\s\d{4}\s\d{4}\b",
    "PAN": r"\b[A-Z]{5}[0-9]{4}[A-Z]\b",
    "UPI_ID": r"\b[a-zA-Z0-9.\-_]+@[a-zA-Z]{3,}\b",
    "IFSC": r"\b[A-Z]{4}0[A-Z0-9]{6}\b"
}

SEVERITY_MAP = {
    "AADHAR": "HIGH",
    "PAN": "HIGH",
    "PASSPORT_IN": "HIGH",
    "VOTER_ID": "HIGH",
    "DL_NUMBER": "HIGH",
    "INDIAN_PHONE": "MEDIUM",
    "EMAIL": "MEDIUM",
    "UPI_ID": "MEDIUM",
    "IFSC": "LOW",
    "LOCATION": "LOW"
}

CONFIDENCE = {
    "REGEX": 0.90
}

def extract_pii(text: str) -> Dict:
    start_time = time.time()
    violations: List[Dict] = []
    
    processed_text = preprocess_for_ner(text)

    for pii_type, pattern in REGEX_PATTERNS.items():
        for match in re.finditer(pattern, processed_text):
            violations.append({
                "type": pii_type,
                "text": match.group(),
                "start": match.start(),
                "end": match.end(),
                "source": "REGEX",
                "confidence": CONFIDENCE["REGEX"],
                "severity": SEVERITY_MAP.get(pii_type, "LOW")
            })

    llm_violations = extract_pii_with_llm(processed_text)
    violations.extend(llm_violations)

    unique_violations = []
    
    sorted_violations = sorted(
        violations,
        key=lambda x: (0 if x["source"] == "LLM" else 1, -(x["end"] - x["start"]))
    )

    def is_overlapping(v1, v2):
        return max(v1["start"], v2["start"]) < min(v1["end"], v2["end"])

    for v in sorted_violations:
        overlap = False
        for u in unique_violations:
            if is_overlapping(v, u):
                overlap = True
                break
        if not overlap:
            unique_violations.append(v)
            
    processing_time_ms = round((time.time() - start_time) * 1000, 2)

    return format_detection_response(unique_violations, processing_time_ms)
