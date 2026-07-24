from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
import time

from utils.entity_extraction import extract_pii
from utils.remediation import process_remediation

router = APIRouter()

class TextRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        max_length=10000,
        example="My phone number is 9876543210 and PAN is ABCDE1234F"
    )

class PiiResponse(BaseModel):
    has_violation: bool
    violation_count: int
    violations: list
    processing_time_ms: float

@router.post("/predict", response_model=PiiResponse)
def detect_pii(request: TextRequest):
    start_time = time.time()

    try:
        result = extract_pii(request.text)
        if result.get("has_violation"):
            process_remediation(result.get("violations", []))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="PII detection failed"
        )

    end_time = time.time()

    return {
        "has_violation": result["has_violation"],
        "violation_count": result["violation_count"],
        "violations": result["violations"],
        "processing_time_ms": round((end_time - start_time) * 1000, 2)
    }
