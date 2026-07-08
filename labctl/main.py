import argparse

from labctl import terraform
from labctl.aws import ecs, rds
from labctl.commands.deploy import deploy_api
from labctl.config import ALB_DNS


def show_status():
    print("AWS Enterprise Lab")
    print("==================")
    print()

    print("ECS")
    print("---")
    ecs.status()
    print()

    print("RDS")
    print("---")
    rds.status()
    print()

    print("Application")
    print("-----------")
    print(f"CloudShop API: http://{ALB_DNS}")
    print()
    print("Cost Control")
    print("------------")
    print("Use 'labctl sleep' to stop ECS and RDS.")

def cost():
    print("Estimated Daily Cost")
    print("====================")
    print("Foundation: near $0")
    print("ECR: pennies")
    print("ALB running: about $0.60-$0.80/day")
    print("ECS 1 small Fargate task running: about $0.40-$0.60/day")
    print("RDS db.t4g.micro running: about $0.50-$1.00/day")
    print()
    print("Use:")
    print("  labctl stop ecs")
    print("  labctl stop rds")


def sleep_lab():
    print("Putting lab to sleep...")
    ecs.stop()
    rds.stop()
    print("Sleep command sent. ECS scales down quickly. RDS may take a few minutes.")


def wake_lab():
    print("Waking lab...")
    rds.start()
    ecs.start()
    print("Wake command sent. RDS and ECS may take a few minutes.")


def main():
    parser = argparse.ArgumentParser(description="AWS Enterprise Lab CLI")
    parser.add_argument(
        "command",
        choices=["status", "start", "stop", "logs", "cost", "deploy", "sleep", "wake"],
    )
    parser.add_argument("target", nargs="?")

    args = parser.parse_args()

    if args.command == "status":
        show_status()
    elif args.command == "cost":
        cost()
    elif args.command == "sleep":
        sleep_lab()
    elif args.command == "wake":
        wake_lab()
    elif args.command == "start" and args.target == "ecs":
        ecs.start()
    elif args.command == "stop" and args.target == "ecs":
        ecs.stop()
    elif args.command == "logs" and args.target == "ecs":
        ecs.logs()
    elif args.command == "start" and args.target == "rds":
        rds.start()
    elif args.command == "stop" and args.target == "rds":
        rds.stop()
    elif args.command == "deploy" and args.target == "api":
        deploy_api()
    else:
        print("Examples:")
        print("  labctl status")
        print("  labctl deploy api")
        print("  labctl start ecs")
        print("  labctl stop ecs")
        print("  labctl start rds")
        print("  labctl stop rds")
        print("  labctl sleep")
        print("  labctl wake")
        print("  labctl cost")


if __name__ == "__main__":
    main()
