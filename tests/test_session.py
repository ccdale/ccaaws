from unittest.mock import MagicMock, patch

from ccaaws.session import session


@patch("ccaaws.session.boto3.Session")
def testSessionNoArgs(mockSession: MagicMock) -> None:
    result = session()

    mockSession.assert_called_once_with(profile_name=None, region_name=None)
    assert result is mockSession.return_value


@patch("ccaaws.session.boto3.Session")
def testSessionWithProfileAndRegion(mockSession: MagicMock) -> None:
    result = session(profile="myprofile", region="eu-west-1")

    mockSession.assert_called_once_with(profile_name="myprofile", region_name="eu-west-1")
    assert result is mockSession.return_value
