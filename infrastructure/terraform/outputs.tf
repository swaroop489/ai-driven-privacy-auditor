output "s3_bucket_name" {
  value = aws_s3_bucket.uploads.id
}

output "lambda_function_arn" {
  value = aws_lambda_function.pii_scanner.arn
}

output "lambda_live_alias_arn" {
  value = aws_lambda_alias.live.arn
}

output "lambda_role_arn" {
  value = aws_iam_role.lambda_role.arn
}

output "lambda_error_alarm_name" {
  value = aws_cloudwatch_metric_alarm.lambda_errors.alarm_name
}

output "lambda_duration_alarm_name" {
  value = aws_cloudwatch_metric_alarm.lambda_duration.alarm_name
}
