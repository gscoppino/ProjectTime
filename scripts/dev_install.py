import os
import subprocess
import sys
from subprocess import CalledProcessError

def dev_install():
    try:
        import ProjectTime
    except ImportError:
        subprocess.run(
            ["pip", "install", "--no-deps", "--disable-pip-version-check", "-e", "."],
            cwd=os.environ["PROJECT_DIR"],
            check=True
        )
    except CalledProcessError:
        return 1

    return 0

if __name__ == "__main__":
    sys.exit(dev_install())