import re
import time
from typing import List, Dict
from utils.preprocess import preprocess_for_ner
from utils.response_formatter import format_detection_response
from utils.llm_extraction import extract_pii_with_llm
from utils.vector_search import check_document_similarity

try:
    from transformers import pipeline
    ner_pipeline = pipeline("ner", model="dslim/bert-base-NER", aggregation_strategy="simple")
except ImportError:
    ner_pipeline = None

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
    "LOCATION": "LOW",
    "PER": "MEDIUM",
    "ORG": "LOW"
}

CONFIDENCE = {
    "REGEX": 0.90,
    "BERT": 0.85
}

def extract_pii(text: str) -> Dict:
    start_time = time.time()
    violations: List[Dict] = []
    
    processed_text = preprocess_for_ner(text)

    sim_result = check_document_similarity(processed_text)
    if sim_result and sim_result.get("is_confidential"):
        violations.append({
            "type": "CONFIDENTIAL_DOCUMENT_LEAK",
            "text": "[ENTIRE DOCUMENT FLAGGED]",
            "start": 0,
            "end": len(processed_text),
            "source": "VECTOR_SEARCH",
            "confidence": sim_result["similarity_score"],
            "severity": "HIGH"
        })

    if ner_pipeline:
        try:
            bert_results = ner_pipeline(processed_text)
            for entity in bert_results:
                label = entity.get("entity_group")
                if label in ["PER", "ORG", "LOC"]:
                    mapped_label = "LOCATION" if label == "LOC" else label
                    violations.append({
                        "type": mapped_label,
                        "text": entity.get("word", ""),
                        "start": entity.get("start", 0),
                        "end": entity.get("end", 0),
                        "source": "BERT",
                        "confidence": float(entity.get("score", CONFIDENCE["BERT"])),
                        "severity": SEVERITY_MAP.get(mapped_label, "LOW")
                    })
        except Exception as e:
            print(f"BERT NER failed: {e}")

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

    unique_violations = []
    
    sorted_violations = sorted(
        violations,
        key=lambda x: -(x["end"] - x["start"])
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
            
    # PRE-LLM MASKING: Create a scrubbed payload so the LLM never sees raw PII
    masked_text = processed_text
    # Replace from end to start to avoid index shifting
    for v in sorted(unique_violations, key=lambda x: x["start"], reverse=True):
        if v["source"] != "VECTOR_SEARCH":
            masked_text = masked_text[:v["start"]] + f"[{v['type']}]" + masked_text[v["end"]:]

    # Pass the SAFE payload to Gemini
    llm_violations = extract_pii_with_llm(masked_text)
    
    # Merge LLM contextual violations back with real indices
    for lv in llm_violations:
        found_idx = processed_text.find(lv.get("text", ""))
        if found_idx != -1:
            lv["start"] = found_idx
            lv["end"] = found_idx + len(lv.get("text", ""))
            unique_violations.append(lv)

    processing_time_ms = round((time.time() - start_time) * 1000, 2)

    return format_detection_response(unique_violations, processing_time_ms)
