from typing import List, Dict
import random
import string
from faker import Faker

fake = Faker('en_IN')

def anonymize_pii(text: str, pii_type: str) -> str:
    if not text:
        return text

    if pii_type == "PER":
        return fake.name()
    elif pii_type == "INDIAN_PHONE":
        return f"+91 {''.join(random.choices(string.digits, k=10))}"
    elif pii_type == "EMAIL":
        return fake.email()
    elif pii_type == "AADHAR":
        return f"{random.randint(1000,9999)} {random.randint(1000,9999)} {random.randint(1000,9999)}"
    elif pii_type == "PAN":
        letters = "".join(random.choices(string.ascii_uppercase, k=5))
        digits = "".join(random.choices(string.digits, k=4))
        last_letter = random.choice(string.ascii_uppercase)
        return f"{letters}{digits}{last_letter}"
    elif pii_type == "UPI_ID":
        name = fake.user_name()
        bank = random.choice(["okaxis", "okhdfcbank", "oksbi", "paytm", "ybl"])
        return f"{name}@{bank}"
    elif pii_type == "IFSC":
        bank = "".join(random.choices(string.ascii_uppercase, k=4))
        branch = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
        return f"{bank}0{branch}"
    elif pii_type == "LOCATION":
        return fake.city()
    elif pii_type == "ORG":
        return fake.company()
        
    if len(text) > 4:
        return f"{text[:2]}{'X' * (len(text)-4)}{text[-2:]}"
    return "X" * len(text)

def mask_pii(text: str, pii_type: str) -> str:
    if not text:
        return text

    if pii_type == "AADHAR":
        clean = text.replace(" ", "")
        if len(clean) >= 12:
            return f"XXXX XXXX {clean[-4:]}"
        return "XXXX XXXX XXXX"
    elif pii_type == "PAN":
        if len(text) == 10:
            return f"XXXXX{text[5:9]}X"
        return "XXXXXXXXXX"
    elif pii_type == "INDIAN_PHONE":
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
        parts = text.split("@")
        if len(parts) == 2:
            name, handle = parts
            if len(name) > 2:
                masked_name = f"{name[0]}{'*' * (len(name)-2)}{name[-1]}"
            else:
                masked_name = "*" * len(name)
            return f"{masked_name}@{handle}"
    elif pii_type in ["VOTER_ID", "PASSPORT_IN", "DL_NUMBER"]:
        if len(text) > 4:
            return f"{'X' * (len(text)-3)}{text[-3:]}"
    elif pii_type == "IFSC":
        if len(text) == 11:
            return f"{text[:4]}0XXXXXX"

    if len(text) > 4:
        return f"{text[:2]}{'X' * (len(text)-4)}{text[-2:]}"
    return "X" * len(text)

def format_detection_response(unique_violations: List[Dict], processing_time_ms: float) -> Dict:
    has_high = any(v.get("severity") == "HIGH" for v in unique_violations)
    has_med = any(v.get("severity") == "MEDIUM" for v in unique_violations)
    
    final_action = "ALLOW"
    if has_high:
        final_action = "BLOCK"
    elif has_med:
        final_action = "WARN"
        
    summary = {}
    for v in unique_violations:
        t = v["type"]
        summary[t] = summary.get(t, 0) + 1

    for v in unique_violations:
        v["masked_text"] = mask_pii(v["text"], v["type"])
        v["synthetic_text"] = anonymize_pii(v["text"], v["type"])

    return {
        "has_violation": len(unique_violations) > 0,
        "violation_count": len(unique_violations),
        "final_action": final_action,
        "summary": summary,
        "violations": unique_violations,
        "processing_time_ms": processing_time_ms
    }
