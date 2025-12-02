```
infrastructure/
│
├── terraform/                     # (Optional) IaC using Terraform
│   ├── main.tf                    # Create S3, Lambda, API Gateway, IAM roles
│   ├── variables.tf
│   ├── outputs.tf
│   ├── lambda.tf                  # Lambda definitions
│   ├── s3.tf                      # S3 bucket configs
│   ├── iam.tf                     # IAM roles/policies
│   ├── api_gateway.tf             # API Gateway endpoints
│   └── cloudwatch.tf              # Logging + monitoring
│
├── aws/
│   ├── lambda/
│   │   ├── nlp_processor/         # NLP Lambda microservice
│   │   │   ├── index.js or main.py
│   │   │   ├── package.json or requirements.txt
│   │   │   └── Dockerfile (optional if using container runtime)
│   │   │
│   │   ├── ocr_processor/         # OCR Lambda microservice
│   │   │   ├── index.js or main.py
│   │   │   ├── package.json or requirements.txt
│   │   │   └── Dockerfile
│   │   │
│   │   ├── post_upload_trigger/   # Triggered when S3 object created
│   │   │   ├── index.js
│   │   │   ├── s3_event_sample.json
│   │   │   └── README.md
│   │
│   ├── api-gateway/
│   │   ├── nlp_api.yaml           # REST API for NLP Lambda
│   │   ├── ocr_api.yaml           # REST API for OCR Lambda
│   │   └── routes.md              # Endpoint documentation
│   │
│   ├── iam/
│   │   ├── lambda_role_policy.json
│   │   ├── s3_access_policy.json
│   │   ├── api_gateway_policy.json
│   │   └── cloudwatch_policy.json
│   │
│   ├── s3/
│   │   ├── bucket_policy.json
│   │   ├── bucket_lifecycle.json
│   │   └── event_notification.json # for S3 → Lambda triggers
│   │
│   └── scripts/
│       ├── deploy_lambda.sh        # Zip + upload Lambda
│       ├── deploy_api.sh           # Create/update API Gateway routes
│       ├── validate_iam.sh         # Validate IAM policies
│       └── cleanup.sh              # Delete old versions
│
└── deployment_guide.md             # End-to-end AWS deployment steps



```
