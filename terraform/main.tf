terraform {
  required_version = ">= 1.10"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 6.23.0"
    }
  }

  backend "s3" {
    bucket       = "ludic-web-tfstate"
    key          = "prod/terraform.tfstate"
    region       = "eu-central-1"
    use_lockfile = true
  }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project = var.app_name
    }
  }
}

# CloudFront requires ACM certs to live in us-east-1.
provider "aws" {
  alias  = "us_east_1"
  region = "us-east-1"

  default_tags {
    tags = {
      Project = var.app_name
    }
  }
}
