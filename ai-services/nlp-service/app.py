"""
app.py
------
Entry point for NLP PII Detection Microservice

Compatible with:
- Local development
- AWS App Runner
- AWS Lambda (via Mangum, optional later)
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import time
import logging

from routes.detect import router as detect_router

# =========================
# Logging Configuration
# =========================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)

# =========================
# FastAPI App Initialization
# =========================
app = FastAPI(
    title="AI Privacy Auditor - NLP Service",
    description="Detects PII using NLP (spaCy) + Regex",
    version="1.0.0"
)

# =========================
# CORS Middleware
# =========================
# Backend / API Gateway will call this service
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # Restrict later if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# Request Timing Middleware
# =========================
@app.middleware("http")
async def log_request_time(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = round((time.time() - start_time) * 1000, 2)

    logger.info(
        f"{request.method} {request.url.path} "
        f"status={response.status_code} "
        f"time={duration}ms"
    )

    response.headers["X-Process-Time-ms"] = str(duration)
    return response

# =========================
# Routes
# =========================
app.include_router(detect_router, prefix="/nlp", tags=["PII Detection"])

# =========================
# Health Check (VERY IMPORTANT)
# =========================
@app.get("/health", tags=["Health"])
def health_check():
    """
    Health endpoint for AWS App Runner / Load Balancers
    """
    return {
        "status": "healthy",
        "service": "nlp-pii-detector"
    }

# =========================
# Root Endpoint (Optional)
# =========================
@app.get("/", tags=["Root"])
def root():
    return {
        "message": "AI Privacy Auditor NLP Service is running"
    }
