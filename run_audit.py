"""
Run Bandit against the project source files.

Usage:
    python run_audit.py
"""

import shutil
import subprocess
import sys
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent


def main():
    bandit = shutil.which("bandit")
    if bandit is None:
        print("Bandit is not installed or is not available on PATH.")
        print("Install it with: python -m pip install -r requirements.txt")
        return 1

    targets = [
        str(PROJECT_DIR / "vulnerable_app.py"),
        str(PROJECT_DIR / "secure_app.py"),
    ]

    print("Running Bandit security analysis...")
    print("Targets:")
    for target in targets:
        print(" -", Path(target).name)

    result = subprocess.run(
        [bandit, "-r", *targets, "-f", "txt"],
        check=False,
    )

    print("\nAudit completed with Bandit exit code:", result.returncode)
    print("Note: the vulnerable file is expected to produce findings.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
