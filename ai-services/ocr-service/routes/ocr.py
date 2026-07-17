from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import tempfile
import shutil
import os
import time
import logging

from utils.ocr_engine import extract_text_from_image
from utils.detect_pii import detect_pii_from_text
from utils.text_cleaner import clean_ocr_text

router = APIRouter()
logger = logging.getLogger(__name__)

SUPPORTED_CONTENT_TYPES = [
    "image/png",
    "image/jpeg",
    "image/jpg",
    "image/tiff",
    "image/bmp"
]

@router.post("/ocr")
async def ocr_and_detect_pii(file: UploadFile = File(...)):
    """
    Upload an image and detect PII from it.
    """

    start_time = time.time()

    # Validate file type
    if file.content_type not in SUPPORTED_CONTENT_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type"
        )

    temp_file_path = None

    try:
        
        suffix = os.path.splitext(file.filename)[1] or ".png"

        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            shutil.copyfileobj(file.file, tmp)
            temp_file_path = tmp.name

        logger.info(f"OCR started for file: {file.filename}")

        # OCR Extraction
        extracted_text = extract_text_from_image(temp_file_path)

        if not extracted_text:
            return JSONResponse(
                status_code=200,
                content={
                    "has_violation": False,
                    "violation_count": 0,
                    "violations": [],
                    "message": "No readable text found in image"
                }
            )

        
        # Clean & Detect PII
        cleaned_text = clean_ocr_text(extracted_text)
        pii_result = detect_pii_from_text(cleaned_text)

        processing_time_ms = round((time.time() - start_time) * 1000, 2)

        return {
            "has_violation": pii_result["has_violation"],
            "violation_count": pii_result["violation_count"],
            "violations": pii_result["violations"],
            "extracted_text": cleaned_text[:300],
            "processing_time_ms": processing_time_ms
        }

    except Exception:
        logger.exception("OCR processing failed")
        raise HTTPException(
            status_code=500,
            detail="OCR processing failed"
        )

    finally:
        # Cleanup temp file
        if temp_file_path and os.path.exists(temp_file_path):
            os.remove(temp_file_path)
