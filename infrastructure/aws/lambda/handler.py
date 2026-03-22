import json
import os
import boto3
import urllib.parse
from pymongo import MongoClient
from datetime import datetime

# Import our PII detection logic
from utils.entity_extraction import extract_pii

# Initialize S3 client
s3 = boto3.client('s3')

# MongoDB Connection (using env vars)
MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/privacy_auditor")
client = MongoClient(MONGO_URI)
db = client.get_database()

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
        # For text-based PII, we read the body. For images, we'd use OCR (future scope)
        response = s3.get_object(Bucket=bucket, Key=key)
        content_type = response.get('ContentType', '')
        
        if 'text' in content_type or key.endswith('.txt'):
            raw_content = response['Body'].read().decode('utf-8')
        else:
            # Placeholder: For non-text files, we'd integrate our OCR engine here.
            # To keep this Lambda simple and focused on the event-trigger claim:
            raw_content = f"Binary file detected: {key}. OCR processing would occur here."
            print(raw_content)

        # 3. Perform PII Detection using our Custom NER Model
        print(f"Processing content for key: {key}...")
        scan_result = extract_pii(raw_content)

        # 4. Enrich result with metadata
        scan_record = {
            "source": f"s3://{bucket}/{key}",
            "processed_at": datetime.utcnow(),
            "content_type": content_type,
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
