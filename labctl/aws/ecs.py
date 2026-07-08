from labctl.config import ECS_CLUSTER, ECS_SERVICE
from labctl.utils import run

def status():
    run(
        f"aws ecs describe-services "
        f"--cluster {ECS_CLUSTER} "
        f"--services {ECS_SERVICE} "
        f"--query 'services[0].{{status:status,desired:desiredCount,running:runningCount,pending:pendingCount}}' "
        f"--output table"
    )

def start():
    run(
        f"aws ecs update-service "
        f"--cluster {ECS_CLUSTER} "
        f"--service {ECS_SERVICE} "
        f"--desired-count 1 "
        f"--output table"
    )

def stop():
    run(
        f"aws ecs update-service "
        f"--cluster {ECS_CLUSTER} "
        f"--service {ECS_SERVICE} "
        f"--desired-count 0 "
        f"--output table"
    )

def logs():
    run("aws logs tail /ecs/aws-cloud-lab-dev-api --since 30m")
