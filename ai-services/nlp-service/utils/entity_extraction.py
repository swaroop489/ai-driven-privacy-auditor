"""
entity_extraction.py
--------------------
Hybrid PII detection using:
1. Custom spaCy NER (fine-tuned for Indian PII)
2. Regex rules (deterministic fallback)

This file is the CORE intelligence of the entire system.
"""

import re
import spacy
import os
from typing import List, Dict
from utils.preprocess import preprocess_for_ner
from utils.response_formatter import format_detection_response

# =========================
# Load spaCy Model
# =========================
# Try loading the custom Indian PII model first.
# Fallback to the generic one if custom doesn't exist.
CUSTOM_MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "model", "custom_indian_pii")

try:
    print(f"Attempting to load custom model from: {CUSTOM_MODEL_PATH}")
    nlp = spacy.load(CUSTOM_MODEL_PATH)
    print("Custom Indian PII model loaded successfully.")
    USING_CUSTOM_MODEL = True
except Exception as e:
    print(f"Warning: Could not load custom model ({e}). Falling back to en_core_web_sm.")
    nlp = spacy.load("en_core_web_sm")
    USING_CUSTOM_MODEL = False

# =========================
# Regex Patterns (Fallback)
# =========================
REGEX_PATTERNS = {
    "EMAIL": r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b",
    "INDIAN_PHONE": r"\b(\+91[\-\s]?)?[6-9]\d{9}\b",
    "AADHAR": r"\b\d{4}\s\d{4}\s\d{4}\b",
    "PAN": r"\b[A-Z]{5}[0-9]{4}[A-Z]\b",
    "UPI_ID": r"\b[a-zA-Z0-9.\-_]+@[a-zA-Z]{3,}\b",
    "IFSC": r"\b[A-Z]{4}0[A-Z0-9]{6}\b"
}

# =========================
# Severity Policy
# =========================
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
    "LOCATION": "LOW",
    "GPE": "LOW",
    "LOC": "LOW"
}

# =========================
# Confidence Scores
# =========================
CONFIDENCE = {
    "CUSTOM_NER": 0.95,
    "GENERIC_NER": 0.85,
    "REGEX": 0.90
}

# =========================
# Main Extraction Function
# =========================
def extract_pii(text: str) -> Dict:
    """
    Analyze text and return structured PII violations
    """
    import time
    start_time = time.time()
    
    violations: List[Dict] = []
    
    # 1. Preprocess text (clean OCR noise, normalize)
    processed_text = preprocess_for_ner(text)

    # 2. spaCy NER Detection
    doc = nlp(processed_text)

    for ent in doc.ents:
        label = ent.label_
        
        # Determine source and confidence based on the model loaded
        source = "CUSTOM_NER" if USING_CUSTOM_MODEL else "GENERIC_NER"
        conf = CONFIDENCE["CUSTOM_NER"] if USING_CUSTOM_MODEL else CONFIDENCE["GENERIC_NER"]
        
        # Only accept relevant labels
        if label in SEVERITY_MAP:
            violations.append({
                "type": label if label not in ["GPE", "LOC"] else "LOCATION",
                "text": ent.text,
                "start": ent.start_char,
                "end": ent.end_char,
                "source": source,
                "confidence": conf,
                "severity": SEVERITY_MAP.get(label, "LOW")
            })

    # 3. Regex-Based Detection (Fallback net)
    for pii_type, pattern in REGEX_PATTERNS.items():
        for match in re.finditer(pattern, processed_text):
            violations.append({
                "type": pii_type,
                "text": match.group(),
                "start": match.start(),
                "end": match.end(),
                "source": "REGEX_FALLBACK",
                "confidence": CONFIDENCE["REGEX"],
                "severity": SEVERITY_MAP.get(pii_type, "LOW")
            })

    # 4. Deduplication
    unique_violations = []
    # We prioritize NER over REGEX_FALLBACK if the text spans overlap
    
    # Sort violations: NLP matches first, then longer matches
    sorted_violations = sorted(
        violations,
        key=lambda x: (0 if "NER" in x["source"] else 1, -(x["end"] - x["start"]))
    )

    # Simple overlap detection
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

    # 5. Build final API response
    return format_detection_response(unique_violations, processing_time_ms)


# =========================
# Local Test (Optional)
# =========================
if __name__ == "__main__":
    sample_text = """
    My phone number is 9876543210.
    My PAN is ABCDE1234F.
    I live in Pune, Maharashtra.
    Email me at test.user@gmail.com.
    Please send payment to rahul@oksbi.
    My Aadhar number is 1234 5678 9012.
    """

    result = extract_pii(sample_text)
    import json
    print(json.dumps(result, indent=2))
