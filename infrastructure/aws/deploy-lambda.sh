#!/bin/bash

# Configuration
AWS_REGION="us-east-1"
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
REPO_NAME="privacy-auditor-lambda"
IMAGE_TAG="latest"
ECR_URL="${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"

echo "------------------------------------------------"
echo "Deploying Privacy Auditor Lambda to AWS ECR"
echo "------------------------------------------------"

# 1. Login to ECR
aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ECR_URL}

# 2. Create Repository if it doesn't exist
aws ecr create-repository --repository-name ${REPO_NAME} --region ${AWS_REGION} || true

# 3. Build Docker Image (from project root)
cd ../../
docker build -t ${REPO_NAME} -f infrastructure/aws/lambda/Dockerfile .

# 4. Tag and Push
docker tag ${REPO_NAME}:${IMAGE_TAG} ${ECR_URL}/${REPO_NAME}:${IMAGE_TAG}
docker push ${ECR_URL}/${REPO_NAME}:${IMAGE_TAG}

echo "------------------------------------------------"
echo "Final Steps:"
echo "1. Go to AWS Lambda Console"
echo "2. Create function -> Container Image"
echo "3. Select: ${ECR_URL}/${REPO_NAME}:${IMAGE_TAG}"
echo "4. Add S3 trigger (Object Created)"
echo "5. Add Environment Variable: MONGO_URI"
echo "------------------------------------------------"
