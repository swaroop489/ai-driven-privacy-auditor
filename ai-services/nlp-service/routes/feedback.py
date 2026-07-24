from fastapi import APIRouter
from pydantic import BaseModel
import os
from pymongo import MongoClient

router = APIRouter()
from config import settings

MONGO_URI = settings.MONGO_URI
client = MongoClient(MONGO_URI)
db = client.get_database()
feedback_collection = db.get_collection("training_feedback")

class FeedbackRequest(BaseModel):
    text: str
    is_false_positive: bool
    corrected_entities: list

@router.post("/feedback")
def submit_feedback(request: FeedbackRequest):
    feedback_collection.insert_one({
        "text": request.text,
        "is_false_positive": request.is_false_positive,
        "corrected_entities": request.corrected_entities,
        "status": "pending_retrain"
    })
    return {"status": "success", "message": "Feedback queued for LoRA pipeline"}
