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

variable "enable_provisioned_concurrency" {
  description = "Enable provisioned concurrency on the Lambda alias"
  type        = bool
  default     = false
}

variable "provisioned_concurrency_count" {
  description = "Provisioned concurrency count for the live alias"
  type        = number
  default     = 1
}

variable "lambda_error_alarm_threshold" {
  description = "Number of Lambda errors allowed before alarming"
  type        = number
  default     = 1
}

variable "lambda_duration_alarm_threshold_ms" {
  description = "Lambda duration threshold in milliseconds for alarming"
  type        = number
  default     = 25000
}
