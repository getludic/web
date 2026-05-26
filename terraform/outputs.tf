output "ecr_repository_url" {
  description = "ECR repository URL"
  value       = aws_ecr_repository.app.repository_url
}

output "lambda_function_name" {
  description = "Lambda function name (used by CI to update image)"
  value       = aws_lambda_function.app.function_name
}

output "lambda_function_url" {
  description = "Public Function URL. Front with CloudFront + Route53 for a custom domain."
  value       = aws_lambda_function_url.app.function_url
}

output "github_actions_role_arn" {
  description = "IAM role ARN to use as AWS_OIDC_ROLE_ARN in GitHub secrets"
  value       = aws_iam_role.github_actions.arn
}

output "search_index_bucket" {
  description = "S3 bucket name for the prebuilt search index"
  value       = aws_s3_bucket.search_index.bucket
}
