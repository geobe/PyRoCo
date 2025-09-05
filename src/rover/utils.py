from pathlib import Path

def get_project_root() -> Path:
    """
    return path to root directory (go 2 levels up from srv/rover).
    """
    return Path(__file__).resolve().parent.parent.parent
