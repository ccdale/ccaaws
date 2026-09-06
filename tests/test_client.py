from unittest.mock import MagicMock, patch

from ccaaws.session import client


@patch("ccaaws.session.session")
def testClientCreatesSessionWhenNoneGiven(mockSession: MagicMock) -> None:
    result = client("s3", profile="myprofile", region="eu-west-1")

    mockSession.assert_called_once_with(profile="myprofile", region="eu-west-1")
    mockSession.return_value.client.assert_called_once_with("s3")
    assert result is mockSession.return_value.client.return_value


@patch("ccaaws.session.session")
def testClientUsesGivenSession(mockSession: MagicMock) -> None:
    givenSess = MagicMock()

    result = client("ec2", sess=givenSess, aws_kwarg="value")

    mockSession.assert_not_called()
    givenSess.client.assert_called_once_with("ec2", aws_kwarg="value")
    assert result is givenSess.client.return_value
