#!/usr/bin/env python3
import argparse
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEV_DIR = ROOT / "infra" / "envs" / "dev"

def run(cmd):
    return subprocess.run(cmd, cwd=DEV_DIR, shell=True, text=True).returncode

def status():
    print("AWS Enterprise Lab")
    print("==================")
    run("terraform output")
    print()
    run("aws ecs describe-services --cluster aws-cloud-lab-dev-cluster --services aws-cloud-lab-dev-api-service --query 'services[0].{status:status,desired:desiredCount,running:runningCount,pending:pendingCount}' --output table")

def start_ecs():
    run("aws ecs update-service --cluster aws-cloud-lab-dev-cluster --service aws-cloud-lab-dev-api-service --desired-count 1 --output table")

def stop_ecs():
    run("aws ecs update-service --cluster aws-cloud-lab-dev-cluster --service aws-cloud-lab-dev-api-service --desired-count 0 --output table")

def logs_ecs():
    run("aws logs tail /ecs/aws-cloud-lab-dev-api --since 30m")

def cost():
    print("Estimated if ECS + ALB running: about $1.00-$1.50/day")
    print("Estimated if ECS stopped but ALB exists: about $0.60-$0.80/day")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["status", "start", "stop", "logs", "cost"])
    parser.add_argument("target", nargs="?")
    args = parser.parse_args()

    if args.command == "status":
        status()
    elif args.command == "start" and args.target == "ecs":
        start_ecs()
    elif args.command == "stop" and args.target == "ecs":
        stop_ecs()
    elif args.command == "logs" and args.target == "ecs":
        logs_ecs()
    elif args.command == "cost":
        cost()
    else:
        print("Examples: ./labctl status | ./labctl start ecs | ./labctl stop ecs | ./labctl logs ecs | ./labctl cost")

if __name__ == "__main__":
    main()
