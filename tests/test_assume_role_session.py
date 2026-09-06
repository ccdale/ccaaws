from unittest.mock import MagicMock, patch

from ccaaws.session import assumeRoleSession


@patch("ccaaws.session.boto3.Session")
@patch("ccaaws.session.session")
def testAssumeRoleSessionCreatesSessionWhenNoneGiven(
    mockSession: MagicMock, mockBotoSession: MagicMock
) -> None:
    givenSess = mockSession.return_value
    givenSess.region_name = "eu-west-1"
    sts = givenSess.client.return_value
    sts.assume_role.return_value = {
        "Credentials": {
            "AccessKeyId": "AKIA",
            "SecretAccessKey": "secret",
            "SessionToken": "token",
        }
    }

    result = assumeRoleSession(
        "arn:aws:iam::123456789012:role/myrole",
        "mysession",
        profile="myprofile",
    )

    mockSession.assert_called_once_with(profile="myprofile", region=None)
    givenSess.client.assert_called_once_with("sts")
    sts.assume_role.assert_called_once_with(
        RoleArn="arn:aws:iam::123456789012:role/myrole",
        RoleSessionName="mysession",
        DurationSeconds=3600,
    )
    mockBotoSession.assert_called_once_with(
        aws_access_key_id="AKIA",
        aws_secret_access_key="secret",
        aws_session_token="token",
        region_name="eu-west-1",
    )
    assert result is mockBotoSession.return_value


@patch("ccaaws.session.boto3.Session")
def testAssumeRoleSessionUsesGivenSession(mockBotoSession: MagicMock) -> None:
    givenSess = MagicMock()
    givenSess.region_name = "us-east-1"
    sts = givenSess.client.return_value
    sts.assume_role.return_value = {
        "Credentials": {
            "AccessKeyId": "AKIA",
            "SecretAccessKey": "secret",
            "SessionToken": "token",
        }
    }

    result = assumeRoleSession(
        "arn:aws:iam::123456789012:role/myrole",
        "mysession",
        sess=givenSess,
        region="ap-south-1",
        duration_seconds=900,
    )

    sts.assume_role.assert_called_once_with(
        RoleArn="arn:aws:iam::123456789012:role/myrole",
        RoleSessionName="mysession",
        DurationSeconds=900,
    )
    mockBotoSession.assert_called_once_with(
        aws_access_key_id="AKIA",
        aws_secret_access_key="secret",
        aws_session_token="token",
        region_name="ap-south-1",
    )
    assert result is mockBotoSession.return_value
