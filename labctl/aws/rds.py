from labctl.config import RDS_INSTANCE
from labctl.utils import run

def status():
    run(
        f"aws rds describe-db-instances "
        f"--db-instance-identifier {RDS_INSTANCE} "
        f"--query 'DBInstances[0].{{status:DBInstanceStatus,endpoint:Endpoint.Address}}' "
        f"--output table"
    )

def start():
    run(
        f"aws rds start-db-instance "
        f"--db-instance-identifier {RDS_INSTANCE} "
        f"--output table"
    )

def stop():
    run(
        f"aws rds stop-db-instance "
        f"--db-instance-identifier {RDS_INSTANCE} "
        f"--output table"
    )
