import json
import os
import boto3
import urllib.parse
import urllib.request
import urllib.error
import uuid
from pymongo import MongoClient
from datetime import datetime

# Import our PII detection logic
from utils.entity_extraction import extract_pii

# Initialize S3 client
s3 = boto3.client('s3')
OCR_SERVICE_URL = os.environ.get("OCR_SERVICE_URL")
NLP_SERVICE_URL = os.environ.get("NLP_SERVICE_URL")

# MongoDB Connection (using env vars)
MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/privacy_auditor")
client = MongoClient(MONGO_URI)
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
        nlp_result = extract_pii(extracted_text)

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
        scan_result = extract_pii(raw_content)

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
        # 1. Parse S3 Event
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
        
        print(f"Received event for bucket: {bucket}, key: {key}")

        # 2. Download content from S3
        response = s3.get_object(Bucket=bucket, Key=key)
        content_type = response.get('ContentType', '')
        body_bytes = response['Body'].read()
        
        if 'text' in content_type or key.endswith('.txt'):
            raw_content = body_bytes.decode('utf-8', errors='ignore')
            scan_result = _scan_text(bucket, key, content_type, raw_content)
        elif content_type.startswith("image/") or key.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp')):
            scan_result = _scan_image(bucket, key, content_type, body_bytes)
        else:
            raw_content = body_bytes.decode('utf-8', errors='ignore')
            scan_result = _scan_text(bucket, key, content_type, raw_content)

        # 3. Enrich result with metadata
        scan_record = {
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
        scans_col = db.get_collection("scans")
        insert_result = scans_col.insert_one(scan_record)
        
        print(f"Successfully processed {key}. ID: {insert_result.inserted_id}")

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Scan completed',
                'id': str(insert_result.inserted_id),
                'action': scan_record["final_action"]
            })
        }

    except Exception as e:
        print(f"Error processing S3 event: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
