from fastapi import APIRouter
from pydantic import BaseModel
import google.generativeai as genai
from utils.vector_search import check_document_similarity, confidential_collection, get_embedding, cosine_similarity
import numpy as np
from config import settings

router = APIRouter()
genai.configure(api_key=settings.GEMINI_API_KEY)

class ChatRequest(BaseModel):
    query: str

def get_relevant_context(query: str):
    if not confidential_collection: return ""
    query_vec = get_embedding(query)
    if query_vec is None: return ""
    
    docs = list(confidential_collection.find({"is_active": {"$ne": False}}))
    best_match = None
    highest_score = 0.0
    
    for doc in docs:
        if "vector" in doc and doc["vector"]:
            db_vec = np.array(doc["vector"])
            score = cosine_similarity(query_vec, db_vec)
            if score > highest_score:
                highest_score = score
                best_match = doc
                
    if highest_score >= 0.5 and best_match:
        return best_match.get("text", "")
    return ""

@router.post("/chat")
def chat_with_docs(request: ChatRequest):
    try:
        context = get_relevant_context(request.query)
        if not context:
            prompt = f"You are a helpful privacy auditor assistant. Answer the user's question:\n{request.query}"
        else:
            prompt = f"You are a helpful privacy auditor assistant. Answer the user's question based ONLY on this confidential context:\n{context}\n\nQuestion: {request.query}"
            
        model = genai.GenerativeModel(settings.GEMINI_MODEL_NAME)
        response = model.generate_content(prompt)
        
        return {"response": response.text, "context_found": bool(context)}
    except Exception as e:
        return {"response": "I'm sorry, the chat service is currently unavailable.", "error": str(e)}
