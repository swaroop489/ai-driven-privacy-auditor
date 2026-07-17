"""
detect.py
---------
FastAPI route for NLP-based PII detection.
This exposes a /predict endpoint.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
import time

from utils.entity_extraction import extract_pii

router = APIRouter()


# Request Schema

class TextRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        max_length=10000,
        example="My phone number is 9876543210 and PAN is ABCDE1234F"
    )



# Response Schema

class PiiResponse(BaseModel):
    has_violation: bool
    violation_count: int
    violations: list
    processing_time_ms: float



# API Route

@router.post("/predict", response_model=PiiResponse)
def detect_pii(request: TextRequest):
    """
    Detect PII entities in given text using NLP + Regex
    """

    start_time = time.time()

    try:
        result = extract_pii(request.text)

    except Exception as e:
        # NEVER leak internal errors
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
