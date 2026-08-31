# grade.py
import subprocess
from pathlib import Path

def grade(workspace):
    result = subprocess.run(
        ["python", "-m", "pytest", "-q"],
        cwd=workspace, capture_output=True, text=True, timeout=60,
    )
    return {"passed": result.returncode == 0, "output": result.stdout[-2000:]}