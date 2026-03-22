"""
response_formatter.py
---------------------
Formats the PII detection results according to the backend API specification.
Handles redaction/masking logic for different entity types.
"""

from typing import List, Dict

def mask_pii(text: str, pii_type: str) -> str:
    """
    Applies type-specific redaction rules to PII strings.
    """
    if not text:
        return text

    if pii_type == "AADHAR":
        # Format: 1234 5678 9012 -> XXXX XXXX 9012
        clean = text.replace(" ", "")
        if len(clean) >= 12:
            return f"XXXX XXXX {clean[-4:]}"
        return "XXXX XXXX XXXX"
        
    elif pii_type == "PAN":
        # Format: ABCDE1234F -> XXXXX1234X
        if len(text) == 10:
            return f"XXXXX{text[5:9]}X"
        return "XXXXXXXXXX"
        
    elif pii_type == "INDIAN_PHONE":
        # Format: +91 9876543210 -> +91 XXXXXX3210
        masked = list(text)
        digits_kept = 0
        digits_masked = 0
        for i in range(len(masked)-1, -1, -1):
            if masked[i].isdigit():
                if digits_kept < 4:
                    digits_kept += 1
                elif digits_masked < 6:
                    masked[i] = "X"
                    digits_masked += 1
        return "".join(masked)
        
    elif pii_type == "EMAIL":
        # Format: user@gmail.com -> u***r@gmail.com
        parts = text.split("@")
        if len(parts) == 2:
            name, domain = parts
            if len(name) > 2:
                masked_name = f"{name[0]}{'*' * (len(name)-2)}{name[-1]}"
            else:
                masked_name = "*" * len(name)
            return f"{masked_name}@{domain}"
        return "***@***.com"

    elif pii_type == "UPI_ID":
        # Format: rahul123@oksbi -> r***3@oksbi
        parts = text.split("@")
        if len(parts) == 2:
            name, handle = parts
            if len(name) > 2:
                masked_name = f"{name[0]}{'*' * (len(name)-2)}{name[-1]}"
            else:
                masked_name = "*" * len(name)
            return f"{masked_name}@{handle}"
        
    elif pii_type in ["VOTER_ID", "PASSPORT_IN", "DL_NUMBER"]:
        # Show only last 3 chars
        if len(text) > 4:
            return f"{'X' * (len(text)-3)}{text[-3:]}"
            
    elif pii_type == "IFSC":
        if len(text) == 11:
            return f"{text[:4]}0XXXXXX"

    # Default fallback: redact almost everything
    if len(text) > 4:
        return f"{text[:2]}{'X' * (len(text)-4)}{text[-2:]}"
    return "X" * len(text)

def format_detection_response(unique_violations: List[Dict], processing_time_ms: float) -> Dict:
    """
    Builds the final API response object for PII detection.
    """
    
    # Calculate overall risk score/status based on severity
    has_high = any(v.get("severity") == "HIGH" for v in unique_violations)
    has_med = any(v.get("severity") == "MEDIUM" for v in unique_violations)
    
    final_action = "ALLOW"
    if has_high:
        final_action = "BLOCK"
    elif has_med:
        final_action = "WARN"
        
    # Group by type for summary
    summary = {}
    for v in unique_violations:
        t = v["type"]
        summary[t] = summary.get(t, 0) + 1

    # Add masked values to the violations list
    for v in unique_violations:
        v["masked_text"] = mask_pii(v["text"], v["type"])

    return {
        "has_violation": len(unique_violations) > 0,
        "violation_count": len(unique_violations),
        "final_action": final_action,
        "summary": summary,
        "violations": unique_violations,
        "processing_time_ms": processing_time_ms
    }
