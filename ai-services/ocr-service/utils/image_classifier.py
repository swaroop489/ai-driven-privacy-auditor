from PIL import Image
import os
import logging

logger = logging.getLogger(__name__)

try:
    from transformers import pipeline
    logger.info("Loading Zero-Shot Image Classification model (CLIP)...")
    classifier = pipeline("zero-shot-image-classification", model="openai/clip-vit-base-patch32")
    logger.info("CLIP model loaded.")
except ImportError:
    classifier = None
except Exception as e:
    logger.error(f"Failed to load CLIP model: {e}")
    classifier = None

CANDIDATE_LABELS = [
    "id card",
    "credit card",
    "passport",
    "driver license",
    "document",
    "screenshot",
    "selfie",
    "nature",
    "other"
]

HIGH_RISK_LABELS = [
    "id card",
    "credit card",
    "passport",
    "driver license"
]

def classify_image(image_path: str) -> dict:
    if not classifier:
        return {"label": "unknown", "score": 0.0, "is_high_risk": False}
    
    try:
        image = Image.open(image_path).convert("RGB")
        results = classifier(image, candidate_labels=CANDIDATE_LABELS)
        
        # Results is a list sorted by highest score
        top_result = results[0]
        
        # We only flag if confidence is > 50%
        is_high_risk = top_result["label"] in HIGH_RISK_LABELS and top_result["score"] > 0.5
        
        return {
            "label": top_result["label"],
            "score": round(top_result["score"], 4),
            "is_high_risk": is_high_risk
        }
    except Exception as e:
        logger.error(f"Image classification failed: {e}")
        return {"label": "unknown", "score": 0.0, "is_high_risk": False}
