import json
from unittest.mock import MagicMock, patch

from ccaaws.s3 import s3GetJson, s3PutJson


@patch("ccaaws.s3.client")
def testS3GetJsonParsesBody(mockClient: MagicMock) -> None:
    s3 = mockClient.return_value
    s3.get_object.return_value = {"Body": MagicMock(read=lambda: b'{"a": 1}')}

    result = s3GetJson("mybucket", "mykey", profile="myprofile")

    mockClient.assert_called_once_with("s3", sess=None, profile="myprofile", region=None)
    s3.get_object.assert_called_once_with(Bucket="mybucket", Key="mykey")
    assert result == {"a": 1}


@patch("ccaaws.s3.client")
def testS3PutJsonEncodesBody(mockClient: MagicMock) -> None:
    s3 = mockClient.return_value

    s3PutJson("mybucket", "mykey", {"a": 1}, region="eu-west-1")

    mockClient.assert_called_once_with("s3", sess=None, profile=None, region="eu-west-1")
    s3.put_object.assert_called_once_with(
        Bucket="mybucket",
        Key="mykey",
        Body=json.dumps({"a": 1}).encode("utf-8"),
        ContentType="application/json",
    )
