resource "aws_cloudwatch_log_group" "app" {
  name              = "/aws/lambda/${var.app_name}"
  retention_in_days = 30
}

resource "aws_lambda_function" "app" {
  function_name = var.app_name
  role          = aws_iam_role.lambda.arn
  package_type  = "Image"
  image_uri     = "${aws_ecr_repository.app.repository_url}:${var.image_tag}"
  architectures = ["x86_64"]
  memory_size   = var.lambda_memory_mb
  timeout       = var.lambda_timeout_s

  environment {
    variables = {
      INDEX_S3_BUCKET = aws_s3_bucket.search_index.bucket
      # AWS Lambda Web Adapter reads PORT to know where to proxy.
      PORT = "8000"
      # Run lifespan startup once during INIT so first request is fast.
      AWS_LWA_ASYNC_INIT           = "true"
      AWS_LWA_READINESS_CHECK_PATH = "/status"
    }
  }

  lifecycle {
    # CI updates image_uri via `aws lambda update-function-code` after each
    # push. Terraform shouldn't fight that.
    ignore_changes = [image_uri]
  }

  depends_on = [
    aws_cloudwatch_log_group.app,
    aws_iam_role_policy_attachment.lambda_basic,
  ]
}

resource "aws_lambda_function_url" "app" {
  function_name      = aws_lambda_function.app.function_name
  authorization_type = "AWS_IAM"
}
