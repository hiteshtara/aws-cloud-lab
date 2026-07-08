from labctl.config import ROOT, ECR_IMAGE, ECS_CLUSTER, ECS_SERVICE
from labctl.utils import run

def deploy_api():
    api_dir = ROOT / "app" / "api"

    print("Building API image for linux/amd64...")
    run(
        "docker buildx build --platform linux/amd64 -t cloudshop-api:latest --load .",
        cwd=api_dir,
        check=True
    )

    print("Tagging image...")
    run(f"docker tag cloudshop-api:latest {ECR_IMAGE}", check=True)

    print("Pushing image to ECR...")
    run(f"docker push {ECR_IMAGE}", check=True)

    print("Redeploying ECS service...")
    run(
        f"aws ecs update-service "
        f"--cluster {ECS_CLUSTER} "
        f"--service {ECS_SERVICE} "
        f"--force-new-deployment",
        check=True
    )

    print("Deploy started. Run: labctl status")
