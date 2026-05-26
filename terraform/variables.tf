variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "eu-central-1"
}

variable "app_name" {
  description = "Application name used for resource naming"
  type        = string
  default     = "ludic-web"
}

variable "github_repo" {
  description = "GitHub repository in 'org/name' form, used for OIDC trust policy"
  type        = string
  default     = "getludic/web"
}

variable "image_tag" {
  description = "Initial Docker image tag for the Lambda function. CI overwrites this on every deploy via update-function-code."
  type        = string
  default     = "latest"
}

variable "lambda_memory_mb" {
  description = "Lambda memory in MB (CPU scales with memory)"
  type        = number
  default     = 1024
}

variable "lambda_timeout_s" {
  description = "Lambda request timeout in seconds (max 900)"
  type        = number
  default     = 30
}

variable "create_github_oidc_provider" {
  description = "Whether to create the GitHub Actions OIDC provider. Set false if it already exists in the account."
  type        = bool
  default     = true
}
