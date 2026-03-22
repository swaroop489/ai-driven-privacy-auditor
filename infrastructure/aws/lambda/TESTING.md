# AWS Lambda - Local Testing Guide

Your Lambda function uses the **AWS Lambda Runtime Interface Emulator (RIE)**. This allows you to test the PII scanning logic locally before pushing it to AWS.

## 1. Build the image
From the project root:
```bash
docker build -t privacy-auditor-lambda -f infrastructure/aws/lambda/Dockerfile .
```

## 2. Run the container locally
You need to pass your MongoDB Atlas URI as an environment variable.
```bash
docker run -p 9000:8080 \
  -e MONGO_URI="your_mongodb_atlas_uri" \
  privacy-auditor-lambda
```

## 3. Invoke the function
Open a new terminal and send a mock S3 event using `curl`:
```bash
curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{
  "Records": [
    {
      "s3": {
        "bucket": { "name": "test-bucket" },
        "object": { "key": "sample_document.txt" }
      }
    }
  ]
}'
```

*Note: The Lambda will attempt to download `sample_document.txt` from S3. If you haven't configured AWS credentials in the container, it will fail on the download step, but you will see the logs showing the PII detection attempt.*
