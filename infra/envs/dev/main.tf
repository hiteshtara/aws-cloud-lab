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

module "networking" {
  source = "../../../terraform/modules/networking"

  project_name = var.project_name
  environment  = local.environment

  vpc_cidr = "10.0.0.0/16"

  availability_zones = [
    "us-east-1a",
    "us-east-1b"
  ]

  public_subnet_cidrs = [
    "10.0.1.0/24",
    "10.0.2.0/24"
  ]

  private_subnet_cidrs = [
    "10.0.101.0/24",
    "10.0.102.0/24"
  ]
}

output "vpc_id" {
  value = module.networking.vpc_id
}

output "public_subnet_ids" {
  value = module.networking.public_subnet_ids
}

output "private_subnet_ids" {
  value = module.networking.private_subnet_ids
}

module "ecr" {
  source = "../../../terraform/modules/ecr"

  repository_name = "${local.name_prefix}-api"
}

output "ecr_repository_url" {
  value = module.ecr.repository_url
}

module "ecs_fargate" {
  source = "../../../terraform/modules/ecs-fargate"

  project_name       = var.project_name
  environment        = local.environment
  vpc_id             = module.networking.vpc_id
  public_subnet_ids  = module.networking.public_subnet_ids
  private_subnet_ids = module.networking.private_subnet_ids

  container_image = "${module.ecr.repository_url}:latest"
}

output "ecs_alb_dns_name" {
  value = module.ecs_fargate.alb_dns_name
}

output "ecs_cluster_name" {
  value = module.ecs_fargate.ecs_cluster_name
}

output "ecs_service_name" {
  value = module.ecs_fargate.ecs_service_name
}
module "rds_postgres" {
  source = "../../../terraform/modules/rds-postgres"

  project_name          = var.project_name
  environment           = local.environment
  vpc_id                = module.networking.vpc_id
  private_subnet_ids    = module.networking.private_subnet_ids
  ecs_security_group_id = module.ecs_fargate.ecs_security_group_id
}

output "db_endpoint" {
  value = module.rds_postgres.db_endpoint
}

output "db_secret_arn" {
  value = module.rds_postgres.db_secret_arn
}