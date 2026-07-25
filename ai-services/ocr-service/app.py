from fastapi import FastAPI
from routes.ocr import router as ocr_router
from config import settings

app = FastAPI(title="OCR PII Detection Service")

app.include_router(ocr_router, prefix="/ocr")
