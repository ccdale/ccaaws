from importlib.metadata import PackageNotFoundError, version as _packageVersion

from ccaaws.paramstore import getParameter
from ccaaws.s3 import s3GetJson, s3PutJson
from ccaaws.secretsmanager import getSecret
from ccaaws.session import (
    assumeRoleClient,
    assumeRoleSession,
    client,
    getAccountId,
    paginate,
    session,
)


def getVersion() -> str:
    """Get the installed version of this package."""
    try:
        return _packageVersion("ccaaws")
    except PackageNotFoundError:
        return "0.0.0"


version = getVersion()

__all__ = [
    "assumeRoleClient",
    "assumeRoleSession",
    "client",
    "getAccountId",
    "getParameter",
    "getSecret",
    "paginate",
    "s3GetJson",
    "s3PutJson",
    "session",
    "version",
]
