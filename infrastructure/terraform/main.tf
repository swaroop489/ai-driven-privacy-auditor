terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# 1. S3 Bucket for Document Uploads
resource "aws_s3_bucket" "uploads" {
  bucket_prefix = "privacy-auditor-uploads-"
  force_destroy = true
}

# 2. IAM Role for Lambda
resource "aws_iam_role" "lambda_role" {
  name = "privacy_auditor_lambda_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })
}

# 3. IAM Policy for S3 and CloudWatch
resource "aws_iam_role_policy" "lambda_policy" {
  name = "privacy_auditor_lambda_policy"
  role = aws_iam_role.lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "s3:GetObject",
          "s3:ListBucket"
        ]
        Effect   = "Allow"
        Resource = [
          "${aws_s3_bucket.uploads.arn}",
          "${aws_s3_bucket.uploads.arn}/*"
        ]
      },
      {
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Effect   = "Allow"
        Resource = "arn:aws:logs:*:*:*"
      }
    ]
  })
}

# 4. Lambda Function (Container Image)
resource "aws_lambda_function" "pii_scanner" {
  function_name = "PII_Scanner_Service"
  role          = aws_iam_role.lambda_role.arn
  package_type  = "Image"
  image_uri     = "${var.ecr_repository_url}:latest"

  environment {
    variables = {
      MONGO_URI       = var.mongo_uri
      NLP_SERVICE_URL = var.nlp_service_url
      OCR_SERVICE_URL  = var.ocr_service_url
    }
  }

  timeout     = 30
  memory_size = 512
}

# 5. S3 Bucket Notification to trigger Lambda
resource "aws_s3_bucket_notification" "bucket_notification" {
  bucket = aws_s3_bucket.uploads.id

  lambda_function {
    lambda_function_arn = aws_lambda_function.pii_scanner.arn
    events              = ["s3:ObjectCreated:*"]
  }

  depends_on = [aws_lambda_permission.allow_s3]
}

# 6. Lambda Permission for S3 to invoke
resource "aws_lambda_permission" "allow_s3" {
  statement_id  = "AllowExecutionFromS3Bucket"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.pii_scanner.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.uploads.arn
}
