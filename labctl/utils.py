import subprocess

def run(cmd, cwd=None, check=False):
    return subprocess.run(
        cmd,
        cwd=cwd,
        shell=True,
        text=True,
        check=check
    )
