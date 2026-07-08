from labctl.config import DEV_DIR
from labctl.utils import run

def outputs():
    run("terraform output", cwd=DEV_DIR)
