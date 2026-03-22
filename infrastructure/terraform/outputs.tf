output "s3_bucket_name" {
  value = aws_s3_bucket.uploads.id
}

output "lambda_function_arn" {
  value = aws_lambda_function.pii_scanner.arn
}

output "lambda_role_arn" {
  value = aws_iam_role.lambda_role.arn
}
