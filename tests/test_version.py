import re

from ccaaws import version


def testVersionIsSemver() -> None:
    assert re.match(r"^\d+\.\d+\.\d+$", version)
