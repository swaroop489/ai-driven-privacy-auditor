import pytest
import sys
import os
import json

# Add parent directory to path so we can import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.entity_extraction import extract_pii
from utils.preprocess import preprocess_for_ner, normalize_text, clean_ocr_noise
from utils.response_formatter import mask_pii

# =======================
# Preprocessing Tests
# =======================
def test_normalize_text():
    raw = "This   is \n\na test. "
    clean = normalize_text(raw)
    assert clean == "This is \na test."

def test_clean_ocr_noise():
    raw = "Here is an amount | 500 |"
    clean = clean_ocr_noise(raw)
    assert "|" not in clean

# =======================
# Redaction/Masking Tests
# =======================
def test_mask_aadhar():
    assert mask_pii("1234 5678 9012", "AADHAR") == "XXXX XXXX 9012"

def test_mask_pan():
    assert mask_pii("ABCDE1234F", "PAN") == "XXXXX1234X"

def test_mask_phone():
    assert mask_pii("+91 9876543210", "INDIAN_PHONE") == "+91 XXXXXX3210"

def test_mask_email():
    assert mask_pii("test.user@gmail.com", "EMAIL") == "t*******r@gmail.com"

# =======================
# Entity Extraction Tests
# =======================
def test_single_aadhar():
    text = "My Aadhar number is 1234 5678 9012."
    result = extract_pii(text)
    
    assert result["has_violation"] is True
    assert result["violation_count"] == 1
    assert result["final_action"] == "BLOCK"
    
    violation = result["violations"][0]
    assert violation["type"] == "AADHAR"
    assert violation["severity"] == "HIGH"
    assert violation["masked_text"] == "XXXX XXXX 9012"

def test_single_pan():
    text = "The PAN ABCDE1234F belongs to the company."
    result = extract_pii(text)
    
    assert result["has_violation"] is True
    
    violation = next((v for v in result["violations"] if v["type"] == "PAN"), None)
    assert violation is not None
    assert "ABCDE1234F" in violation["text"]

def test_multiple_pii():
    text = "Name is Rahul. Aadhar: 9876 5432 1098. Phone: +91 9000011111."
    result = extract_pii(text)
    
    assert result["has_violation"] is True
    assert result["violation_count"] >= 2
    
    types = [v["type"] for v in result["violations"]]
    assert "AADHAR" in types
    assert "INDIAN_PHONE" in types

def test_negative_example():
    text = "The weather in Pune is quite pleasant today."
    result = extract_pii(text)
    
    pii_types = [v["type"] for v in result["violations"]]
    for high_severity_type in ["AADHAR", "PAN", "INDIAN_PHONE"]:
        assert high_severity_type not in pii_types

def test_upi_detection():
    text = "Please transfer the amount to rahul.sharma@okicici"
    result = extract_pii(text)
    
    violation = next((v for v in result["violations"] if v["type"] == "UPI_ID"), None)
    assert violation is not None
    assert violation["text"] == "rahul.sharma@okicici"
