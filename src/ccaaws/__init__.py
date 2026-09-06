import subprocess
import tomllib
from pathlib import Path

from ccaaws.session import assumeRoleClient, client, session


def gitRoot() -> str:
    """Get the root directory of the current git repository."""
    try:
        return (
            subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True)
            .splitlines()
            .pop()
        )
    except (subprocess.CalledProcessError, OSError):
        return ""


def getVersion() -> str:
    """Get the version of the project from pyproject.toml."""
    root = gitRoot()
    if not root:
        return "0.0.0"
    pyprojectPath = Path(root) / "pyproject.toml"
    if not pyprojectPath.exists():
        return "0.0.0"
    try:
        with open(pyprojectPath, "rb") as f:
            pyprojectData = tomllib.load(f)
        return pyprojectData.get("project", {}).get("version", "0.0.0")
    except (OSError, tomllib.TOMLDecodeError):
        return "0.0.0"


version = getVersion()

__all__ = ["assumeRoleClient", "client", "session", "version"]
