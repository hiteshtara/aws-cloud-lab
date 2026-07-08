from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEV_DIR = ROOT / "infra" / "envs" / "dev"

AWS_REGION = "us-east-1"

PROJECT_NAME = "aws-cloud-lab"
ENVIRONMENT = "dev"

ECS_CLUSTER = "aws-cloud-lab-dev-cluster"
ECS_SERVICE = "aws-cloud-lab-dev-api-service"

RDS_INSTANCE = "aws-cloud-lab-dev-postgres"

ECR_IMAGE = "589744711110.dkr.ecr.us-east-1.amazonaws.com/aws-cloud-lab-dev-api:latest"

ALB_DNS = "aws-cloud-lab-dev-alb-1066666369.us-east-1.elb.amazonaws.com"
