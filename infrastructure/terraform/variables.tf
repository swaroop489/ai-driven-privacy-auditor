variable "aws_region" {
  description = "AWS region for deployment"
  default     = "us-east-1"
}

variable "ecr_repository_url" {
  description = "The URL of the ECR repository containing the Lambda image"
}

variable "mongo_uri" {
  description = "MongoDB Atlas connection string for the Lambda function"
  sensitive   = true
}

variable "nlp_service_url" {
  description = "Public URL for the NLP microservice"
  default     = ""
}

variable "ocr_service_url" {
  description = "Public URL for the OCR microservice"
  default     = ""
}
