from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from utils.vector_search import add_confidential_document

router = APIRouter()

class ConfidentialDocUpload(BaseModel):
    name: str
    text: str

@router.post("/fingerprint")
async def fingerprint_document(doc: ConfidentialDocUpload):
    success = add_confidential_document(doc.name, doc.text)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to generate vector embedding. Ensure sentence-transformers is loaded.")
    return {"status": "success", "message": f"Successfully generated semantic fingerprint for '{doc.name}'"}
