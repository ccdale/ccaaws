from importlib.metadata import PackageNotFoundError, version as _packageVersion

from ccaaws.session import assumeRoleClient, client, session


def getVersion() -> str:
    """Get the installed version of this package."""
    try:
        return _packageVersion("ccaaws")
    except PackageNotFoundError:
        return "0.0.0"


version = getVersion()

__all__ = ["assumeRoleClient", "client", "session", "version"]
