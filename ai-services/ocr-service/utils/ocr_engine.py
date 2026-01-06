"""
ocr_engine.py
-------------
Core OCR engine for extracting text from images.

Designed to work with:
- Local development
- AWS App Runner
- AWS Lambda (container-based)

Uses Tesseract OCR.
"""

import pytesseract
from PIL import Image
import logging
import os
from typing import Optional

# =========================
# Logging
# =========================
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# =========================
# Tesseract Configuration
# =========================
# App Runner / Lambda container usually has tesseract in PATH
# If needed, set explicit path:
# pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

TESSERACT_CONFIG = r"--oem 3 --psm 6"  
# OEM 3 = default LSTM
# PSM 6 = Assume a uniform block of text

SUPPORTED_FORMATS = (".png", ".jpg", ".jpeg", ".tiff", ".bmp")

# =========================
# OCR Function
# =========================
def extract_text_from_image(image_path: str) -> Optional[str]:
    """
    Extract text from an image file.

    Args:
        image_path (str): Path to image file

    Returns:
        str | None: Extracted text or None if failed
    """

    if not os.path.exists(image_path):
        logger.error(f"Image not found: {image_path}")
        return None

    if not image_path.lower().endswith(SUPPORTED_FORMATS):
        logger.error(f"Unsupported image format: {image_path}")
        return None

    try:
        logger.info(f"Starting OCR for image: {image_path}")

        image = Image.open(image_path)

        # Convert to RGB (important for scanned documents)
        if image.mode != "RGB":
            image = image.convert("RGB")

        text = pytesseract.image_to_string(
            image,
            config=TESSERACT_CONFIG
        )

        cleaned_text = text.strip()

        logger.info("OCR extraction completed successfully")

        return cleaned_text if cleaned_text else None

    except Exception as e:
        logger.exception("OCR extraction failed")
        return None


# =========================
# Local Test (Optional)
# =========================
if __name__ == "__main__":
    sample_image = "tests/test_images/id_sample.jpg"
    extracted = extract_text_from_image(sample_image)

    print("----- OCR OUTPUT -----")
    print(extracted)
