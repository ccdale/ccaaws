from unittest.mock import MagicMock, patch

from ccaaws.session import getAccountId


@patch("ccaaws.session.session")
def testGetAccountIdCreatesSessionWhenNoneGiven(mockSession: MagicMock) -> None:
    sts = mockSession.return_value.client.return_value
    sts.get_caller_identity.return_value = {"Account": "123456789012"}

    result = getAccountId(profile="myprofile", region="eu-west-1")

    mockSession.assert_called_once_with(profile="myprofile", region="eu-west-1")
    mockSession.return_value.client.assert_called_once_with("sts")
    assert result == "123456789012"


@patch("ccaaws.session.session")
def testGetAccountIdUsesGivenSession(mockSession: MagicMock) -> None:
    givenSess = MagicMock()
    givenSess.client.return_value.get_caller_identity.return_value = {"Account": "999999999999"}

    result = getAccountId(sess=givenSess)

    mockSession.assert_not_called()
    assert result == "999999999999"
