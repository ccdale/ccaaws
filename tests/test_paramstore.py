from unittest.mock import MagicMock, patch

from ccaaws.paramstore import getParameter


@patch("ccaaws.paramstore.client")
def testGetParameterReturnsValue(mockClient: MagicMock) -> None:
    ssm = mockClient.return_value
    ssm.get_parameter.return_value = {"Parameter": {"Value": "myvalue"}}

    result = getParameter("/my/param", profile="myprofile", region="eu-west-1")

    mockClient.assert_called_once_with("ssm", sess=None, profile="myprofile", region="eu-west-1")
    ssm.get_parameter.assert_called_once_with(Name="/my/param", WithDecryption=True)
    assert result == "myvalue"


@patch("ccaaws.paramstore.client")
def testGetParameterWithoutDecryption(mockClient: MagicMock) -> None:
    ssm = mockClient.return_value
    ssm.get_parameter.return_value = {"Parameter": {"Value": "myvalue"}}

    getParameter("/my/param", withDecryption=False)

    ssm.get_parameter.assert_called_once_with(Name="/my/param", WithDecryption=False)
