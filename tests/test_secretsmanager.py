from unittest.mock import MagicMock, patch

from ccaaws.secretsmanager import getSecret


@patch("ccaaws.secretsmanager.client")
def testGetSecretReturnsSecretString(mockClient: MagicMock) -> None:
    sm = mockClient.return_value
    sm.get_secret_value.return_value = {"SecretString": "mysecret"}

    result = getSecret("mySecretId", profile="myprofile")

    mockClient.assert_called_once_with("secretsmanager", sess=None, profile="myprofile", region=None)
    sm.get_secret_value.assert_called_once_with(SecretId="mySecretId")
    assert result == "mysecret"


@patch("ccaaws.secretsmanager.client")
def testGetSecretDecodesSecretBinary(mockClient: MagicMock) -> None:
    sm = mockClient.return_value
    sm.get_secret_value.return_value = {"SecretBinary": b"mysecret"}

    result = getSecret("mySecretId")

    assert result == "mysecret"
