import json
import os
import boto3
import urllib.parse
import urllib.request
import urllib.error
import uuid
import time
from pymongo import MongoClient
from datetime import datetime

# Initialize S3 client
s3 = boto3.client('s3')
OCR_SERVICE_URL = os.environ.get("OCR_SERVICE_URL")
NLP_SERVICE_URL = os.environ.get("NLP_SERVICE_URL")
MEDIA_SERVICE_URL = os.environ.get("MEDIA_SERVICE_URL")
ENABLE_LOCAL_FALLBACK = str(os.environ.get("ENABLE_LOCAL_FALLBACK", "false")).lower() == "true"

_cold_start = True

# MongoDB Connection 
MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/privacy_auditor")
client = MongoClient(
    MONGO_URI,
    maxPoolSize=int(os.environ.get("MONGO_MAX_POOL_SIZE", "5")),
    minPoolSize=int(os.environ.get("MONGO_MIN_POOL_SIZE", "0")),
    serverSelectionTimeoutMS=int(os.environ.get("MONGO_SERVER_SELECTION_TIMEOUT_MS", "5000")),
    connectTimeoutMS=int(os.environ.get("MONGO_CONNECT_TIMEOUT_MS", "5000")),
    socketTimeoutMS=int(os.environ.get("MONGO_SOCKET_TIMEOUT_MS", "20000")),
)
db = client.get_database()


def _post_json(url, payload):
    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def _post_multipart(url, file_bytes, filename, content_type):
    boundary = f"----privacy-auditor-{uuid.uuid4().hex}"
    body = []
    body.append(f"--{boundary}\r\n".encode("utf-8"))
    body.append(
        (
            f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'
            f"Content-Type: {content_type}\r\n\r\n"
        ).encode("utf-8")
    )
    body.append(file_bytes)
    body.append(f"\r\n--{boundary}--\r\n".encode("utf-8"))

    request = urllib.request.Request(
        url,
        data=b"".join(body),
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        method="POST",
    )

    with urllib.request.urlopen(request, timeout=60) as response:
        return json.loads(response.read().decode("utf-8"))


def _merge_violations(*groups):
    seen = set()
    merged = []

    for group in groups:
        for violation in group or []:
            text = violation.get("text") or violation.get("maskedText") or ""
            key = (
                violation.get("type"),
                text,
                violation.get("severity"),
                violation.get("confidence"),
            )

            if key in seen:
                continue

            seen.add(key)
            merged.append(violation)

    return merged


def _extract_pii_fallback(text):
    if not ENABLE_LOCAL_FALLBACK:
        return {}
    
    import re
    # Basic failsafe regex if NLP microservice goes down
    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    violations = []
    
    for match in re.finditer(email_pattern, text):
        violations.append({
            "type": "EMAIL",
            "text": match.group(),
            "severity": "MEDIUM",
            "source": "LAMBDA_FALLBACK_REGEX"
        })
        
    return {
        "has_violation": len(violations) > 0,
        "violation_count": len(violations),
        "violations": violations
    }


def _get_uploads_collection():
    return db.get_collection("uploads")


def _get_violations_collection():
    return db.get_collection("violations")


def _get_stats_snapshot():
    uploads = _get_uploads_collection()
    violations = _get_violations_collection()

    return {
        "upload_count": uploads.count_documents({}),
        "violation_count": violations.count_documents({}),
        "high_risk_count": violations.count_documents({"severity": "HIGH"}),
    }


def _update_job(job_id, payload):
    if not job_id:
        return None

    uploads = _get_uploads_collection()
    uploads.update_one(
        {"jobId": job_id},
        {"$set": payload},
        upsert=True,
    )
    return job_id


def _scan_image(bucket, key, content_type, body_bytes):
    if not OCR_SERVICE_URL:
        raise RuntimeError("OCR_SERVICE_URL is required for image scans")

    ocr_result = _post_multipart(
        OCR_SERVICE_URL,
        body_bytes,
        filename=key.split("/")[-1] or "upload.png",
        content_type=content_type or "application/octet-stream",
    )

    extracted_text = (ocr_result.get("extracted_text") or "").strip()
    nlp_result = {}
    if extracted_text and NLP_SERVICE_URL:
        try:
            nlp_result = _post_json(NLP_SERVICE_URL, {"text": extracted_text})
        except Exception as exc:
            print(f"NLP service call failed for {key}: {exc}")

    if not nlp_result and extracted_text:
        nlp_result = _extract_pii_fallback(extracted_text)

    violations = _merge_violations(
        ocr_result.get("violations", []),
        nlp_result.get("violations", []),
    )

    return {
        "source": f"s3://{bucket}/{key}",
        "content_type": content_type,
        "has_violation": bool(violations),
        "violation_count": len(violations),
        "summary": nlp_result.get("summary", ocr_result.get("summary", {})),
        "violations": violations,
        "final_action": nlp_result.get("final_action", ocr_result.get("final_action", "ALLOW")),
        "processing_time_ms": nlp_result.get("processing_time_ms", ocr_result.get("processing_time_ms", 0)),
    }


def _scan_text(bucket, key, content_type, raw_content):
    scan_result = {}

    if NLP_SERVICE_URL:
        try:
            scan_result = _post_json(NLP_SERVICE_URL, {"text": raw_content})
        except Exception as exc:
            print(f"NLP service call failed for {key}: {exc}")

    if not scan_result:
        scan_result = _extract_pii_fallback(raw_content)

    return {
        "source": f"s3://{bucket}/{key}",
        "content_type": content_type,
        "has_violation": scan_result.get("has_violation", False),
        "violation_count": scan_result.get("violation_count", 0),
        "summary": scan_result.get("summary", {}),
        "violations": scan_result.get("violations", []),
        "final_action": scan_result.get("final_action", "ALLOW"),
        "processing_time_ms": scan_result.get("processing_time_ms", 0),
    }

def _scan_media(bucket, key, content_type, body_bytes):
    if not MEDIA_SERVICE_URL:
        raise RuntimeError("MEDIA_SERVICE_URL is required for media scans")
        
    media_result = _post_multipart(
        MEDIA_SERVICE_URL,
        body_bytes,
        filename=key.split("/")[-1] or "upload.mp4",
        content_type=content_type or "application/octet-stream",
    )
    
    scan_result = media_result.get("privacy_scan", {})
    return {
        "source": f"s3://{bucket}/{key}",
        "content_type": content_type,
        "has_violation": scan_result.get("has_violation", False),
        "violation_count": scan_result.get("violation_count", 0),
        "summary": scan_result.get("summary", {}),
        "violations": scan_result.get("violations", []),
        "final_action": scan_result.get("final_action", "ALLOW"),
        "processing_time_ms": scan_result.get("processing_time_ms", 0),
    }

def handler(event, context):
    """
    AWS Lambda handler invoked by S3 events.
    Flow: S3 Put -> Lambda -> Download -> Extract PII -> Save to MongoDB
    """
    try:
        global _cold_start
        invocation_started_at = time.time()
        is_cold_start = _cold_start
        _cold_start = False

        # 1. Parse S3 Event
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
        
        print(f"Received event for bucket: {bucket}, key: {key}, cold_start={is_cold_start}")

        # 2. Download content from S3
        response = s3.get_object(Bucket=bucket, Key=key)
        content_type = response.get('ContentType', '')
        metadata = response.get("Metadata", {}) or {}
        job_id = metadata.get("jobid") or key
        body_bytes = response['Body'].read()

        _update_job(job_id, {
            "status": "PROCESSING",
            "scanMode": "ASYNC",
            "sourceKey": f"s3://{bucket}/{key}",
            "fileUrl": f"s3://{bucket}/{key}",
        })
        
        if 'text' in content_type or key.endswith('.txt'):
            raw_content = body_bytes.decode('utf-8', errors='ignore')
            scan_result = _scan_text(bucket, key, content_type, raw_content)
        elif content_type.startswith("image/") or key.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp')):
            scan_result = _scan_image(bucket, key, content_type, body_bytes)
        elif content_type.startswith("audio/") or content_type.startswith("video/") or key.lower().endswith(('.mp3', '.wav', '.m4a', '.mp4', '.avi', '.mov', '.mkv')):
            scan_result = _scan_media(bucket, key, content_type, body_bytes)
        else:
            raw_content = body_bytes.decode('utf-8', errors='ignore')
            scan_result = _scan_text(bucket, key, content_type, raw_content)

        # 3. Enrich result with metadata
        scan_record = {
            "jobId": job_id,
            "source": scan_result["source"],
            "processed_at": datetime.utcnow(),
            "content_type": scan_result["content_type"],
            "has_violation": scan_result.get("has_violation", False),
            "violation_count": scan_result.get("violation_count", 0),
            "summary": scan_result.get("summary", {}),
            "violations": scan_result.get("violations", []),
            "final_action": scan_result.get("final_action", "ALLOW"),
            "processing_time_ms": scan_result.get("processing_time_ms", 0),
            "trigger": "S3_EVENT"
        }

        # 5. Persist to MongoDB
        print("Saving scan results to MongoDB...")
        uploads_col = _get_uploads_collection()
        update_result = uploads_col.update_one(
            {"jobId": job_id},
            {"$set": {
                **scan_record,
                "status": "COMPLETED",
                "errorMessage": None,
            }},
            upsert=True,
        )

        print(f"Successfully processed {key}. jobId={job_id}, matched={update_result.matched_count}")

        stats_snapshot = _get_stats_snapshot()

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Scan completed',
                'jobId': job_id,
                'action': scan_record["final_action"],
                'coldStart': is_cold_start,
                'invocationTimeMs': round((time.time() - invocation_started_at) * 1000, 2),
                'statsSnapshot': stats_snapshot
            })
        }

    except Exception as e:
        print(f"Error processing S3 event: {str(e)}")
        try:
            _update_job(job_id if 'job_id' in locals() else None, {
                "status": "FAILED",
                "errorMessage": str(e),
            })
        except Exception as update_error:
            print(f"Failed to update job status: {update_error}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
