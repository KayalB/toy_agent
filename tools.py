from pathlib import Path
import subprocess


WORKSPACE = Path("workspace").resolve()


def _resolve(path):
    """Resolve a user-supplied path, refusing anything outside the workspace."""
    target = (WORKSPACE / path).resolve()
    if not target.is_relative_to(WORKSPACE):
        raise ValueError("path escapes the workspace")
    return target


def list_files(path="."):
    """List the immediate contents of a directory in the workspace."""
    try:
        target = _resolve(path)
    except ValueError:
        return f"Error: '{path}' is outside the workspace. Use paths relative to the workspace root, like 'ledger' or '.'."

    if not target.exists():
        return f"Error: '{path}' does not exist. Use list_files('.') to see the workspace root."
    if not target.is_dir():
        return f"Error: '{path}' is a file, not a directory. Use read_file to read it."

    entries = []
    for item in sorted(target.iterdir()):
        if item.name.startswith("."):
            continue
        entries.append(item.name + "/" if item.is_dir() else item.name)

    if not entries:
        return f"'{path}' is empty."
    return "\n".join(entries)


def read_file(fpath):
    """Return a file in the workspace as a string"""
    try:
        target = _resolve(fpath)
    except ValueError:
        return f"Error: '{fpath}' is outside the workspace. Use files relative to the workspace root, like 'ledger/money.py'."

    if not target.exists():
        return f"Error: '{fpath}' does not exist. Use list_files('.') to see the workspace root."
    if target.is_dir():
        return f"Error: '{fpath}' is a directory, not a file. Use list_files to output its contents."

    file_content = target.read_text(encoding="utf-8")
    return file_content


def write_file(fpath, fcontent):
    """Create a new or replace a file in the workspace with a new file passed in as a string"""
    try:
        target = _resolve(fpath)
    except ValueError:
        return f"Error: '{fpath}' is outside the workspace. Use files relative to the workspace root, like 'ledger/money.py'."

    if not target.exists():
        return f"Error: '{fpath}' does not exist. Use list_files('.') to see the workspace root."
    if target.is_dir():
        return f"Error: '{fpath}' is a firectory, not a file. Use list_files to output its contents."

    target.write_text(fcontent)

    return "Success, overwrote workplace/" + fpath

def run_tests():
    """Run pytest in the workspace and return its output."""
    try:
        result = subprocess.run(
            ["python", "-m", "pytest", "-q"],
            cwd=WORKSPACE,
            capture_output=True,
            text=True,
            timeout=60,
        )
    except subprocess.TimeoutExpired:
        return "Error: the test suite timed out after 60 seconds."

    return result.stdout + result.stderr


LIST_FILES = {
    "name": "list_files",
    "description": "List files and directories under a path in the workspace.",
    "input_schema": {
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "Path relative to the workspace root. Use '.' for the root."
            }
        },
        "required": ["path"]
    }
}

READ_FILE = {
    "name": "read_file",
    "description": "Read file under a path in the workspace.",
    "input_schema": {
        "type": "object",
        "properties": {
            "fpath": {
                "type": "string",
                "description": "File path relative to the workspace root."
            }
        },
        "required": ["fpath"]
    }
}

WRITE_FILE = {
    "name": "write_file",
    "description": "Create or overwrite a file under a path in the workspace.",
    "input_schema": {
        "type": "object",
        "properties": {
            "fpath": {
                "type": "string",
                "description": "File path relative to the workspace root."
            }, 
            "fcontent": {
                "type": "string",
                "description": "Conent of entire updated file as a string"
            }
        },
        "required": ["fpath", "fcontent"]
    }
}

RUN_TESTS = {
    "name": "run_tests",
    "description": "Run the test suite. Call this first to see what is failing before reading source files.",
    "input_schema": {
        "type": "object",
        "properties": {},
    },
}



TOOLS = {
    "list_files": (LIST_FILES, list_files),
    "read_file": (READ_FILE, read_file),
    "write_file": (WRITE_FILE, write_file),
    "run_tests": (RUN_TESTS, run_tests),
}

SCHEMAS = [schema for schema, _ in TOOLS.values()]