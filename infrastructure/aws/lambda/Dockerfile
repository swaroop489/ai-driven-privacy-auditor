# Use official AWS Lambda Python base image
FROM public.ecr.aws/lambda/python:3.11

# Set working directory to Lambda task root
WORKDIR ${LAMBDA_TASK_ROOT}

# Copy requirements and install
COPY infrastructure/aws/lambda/requirements.txt .
RUN pip install -r requirements.txt

# Copy our PII Detection model weights
COPY ai-services/nlp-service/model/custom_indian_pii ./model/custom_indian_pii

# Copy the utility functions (preprocess, extraction, response_formatter)
COPY ai-services/nlp-service/utils/ ./utils/

# Copy the Lambda handler code
COPY infrastructure/aws/lambda/handler.py .

# Set the CMD to your handler (filename.method)
CMD [ "handler.handler" ]
