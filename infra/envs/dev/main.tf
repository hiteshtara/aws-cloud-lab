terraform {
  required_version = ">= 1.6.0"

  backend "s3" {
    bucket         = "aws-cloud-lab-tf-state-589744711110"
    key            = "dev/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "aws-cloud-lab-tf-lock"
    encrypt        = true
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    archive = {
      source  = "hashicorp/archive"
      version = "~> 2.4"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

variable "aws_region" {
  default = "us-east-1"
}

variable "project_name" {
  default = "aws-cloud-lab"
}

locals {
  environment = "dev"
  name_prefix = "${var.project_name}-${local.environment}"
}

module "dynamodb" {
  source = "../../modules/dynamodb"

  table_name = "${local.name_prefix}-app"
}

module "lambda" {
  source = "../../modules/lambda"

  function_name      = "${local.name_prefix}-api"
  role_name          = "${local.name_prefix}-lambda-role"
  policy_name        = "${local.name_prefix}-lambda-policy"
  lambda_source_file = "../../../app/lambda/handler.py"
  lambda_zip_file    = "../../../app/lambda/function.zip"
  table_name         = module.dynamodb.table_name
  table_arn          = module.dynamodb.table_arn
}

module "http_api" {
  source = "../../modules/http-api"

  api_name             = "${local.name_prefix}-http-api"
  lambda_function_name = module.lambda.function_name
  lambda_invoke_arn    = module.lambda.invoke_arn
}

output "api_url" {
  value = module.http_api.api_url
}

output "dynamodb_table" {
  value = module.dynamodb.table_name
}

output "lambda_name" {
  value = module.lambda.function_name
}
