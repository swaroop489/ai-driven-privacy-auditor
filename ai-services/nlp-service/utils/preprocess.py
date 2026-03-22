"""
preprocess.py
-------------
Text preprocessing utilities for PII detection.
Handles cleanup of raw text and OCR noise.
"""

import re
import unicodedata

def normalize_text(text: str) -> str:
    """
    Normalizes text for consistent NER processing.
    """
    if not text:
        return ""

    # 1. Normalize unicode (e.g., convert stylized fonts to standard)
    text = unicodedata.normalize('NFKC', text)

    # 2. Replace multiple newlines with a single newline
    text = re.sub(r'\n+', '\n', text)

    # 3. Replace multiple spaces with a single space
    text = re.sub(r'[ \t]+', ' ', text)

    return text.strip()

def clean_ocr_noise(text: str) -> str:
    """
    Cleans up common OCR artifacts before NER processing.
    e.g., common character misrecognitions like O/0, I/1.
    """
    if not text:
        return ""

    # Fix common Aadhar/PAN OCR errors
    # E.g. sometimes "0" (zero) is read as "O" (letter)
    # We apply this somewhat conservatively
    
    # 1. Strip extraneous pipe characters often created by borders
    text = text.replace('|', '')
    
    # 2. Fix common spacing errors in numbers
    # (Leaving this to regex matching in entity extraction as it's safer)
    
    return text.strip()

def preprocess_for_ner(text: str) -> str:
    """
    Full preprocessing pipeline before feeding to spaCy custom NER.
    """
    text = normalize_text(text)
    text = clean_ocr_noise(text)
    return text
