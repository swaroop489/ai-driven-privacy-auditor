import logging
import os
import time

logger = logging.getLogger(__name__)

try:
    import numpy as np
    from transformers import pipeline
    from pymongo import MongoClient
    embedder = pipeline("feature-extraction", model="sentence-transformers/all-MiniLM-L6-v2")
except ImportError:
    embedder = None
    np = None
except Exception:
    embedder = None
    np = None

MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/privacy_auditor")
client = MongoClient(MONGO_URI)
db = client.get_database()
confidential_collection = db.get_collection("confidential_docs")

def get_embedding(text: str):
    if not embedder or not np:
        return None
    try:
        emb = embedder(text)
        vec = np.mean(emb[0], axis=0)
        return vec
    except Exception:
        return None

def cosine_similarity(v1, v2):
    dot_product = np.dot(v1, v2)
    norm_v1 = np.linalg.norm(v1)
    norm_v2 = np.linalg.norm(v2)
    if norm_v1 == 0 or norm_v2 == 0:
        return 0.0
    return dot_product / (norm_v1 * norm_v2)

def check_document_similarity(text: str, threshold: float = 0.85) -> dict:
    if not embedder:
        return None
        
    query_vec = get_embedding(text)
    if query_vec is None:
        return None
        
    best_match = None
    highest_score = 0.0
    
    docs = list(confidential_collection.find({"is_active": {"$ne": False}}))
    
    for doc in docs:
        if "vector" in doc and doc["vector"]:
            db_vec = np.array(doc["vector"])
            score = cosine_similarity(query_vec, db_vec)
        elif "text" in doc and doc["text"]:
            db_vec = get_embedding(doc["text"])
            if db_vec is not None:
                score = cosine_similarity(query_vec, db_vec)
        else:
            continue
            
        if score > highest_score:
            highest_score = score
            best_match = doc.get("name", "Unknown Document")
            
    if highest_score >= threshold:
        return {
            "is_confidential": True,
            "similarity_score": round(float(highest_score), 4),
            "matched_document": best_match
        }
        
    return {"is_confidential": False, "similarity_score": round(float(highest_score), 4)}
