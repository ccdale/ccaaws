"""Helpers for reading and writing JSON objects in S3."""

from __future__ import annotations

import json
from typing import Any

import boto3

from ccaaws.session import client


def s3GetJson(
    bucket: str,
    key: str,
    sess: boto3.Session | None = None,
    profile: str | None = None,
    region: str | None = None,
    **kwargs: Any,
) -> Any:
    """Read an S3 object and parse its body as JSON."""
    s3 = client("s3", sess=sess, profile=profile, region=region)
    obj = s3.get_object(Bucket=bucket, Key=key, **kwargs)
    return json.loads(obj["Body"].read())


def s3PutJson(
    bucket: str,
    key: str,
    data: Any,
    sess: boto3.Session | None = None,
    profile: str | None = None,
    region: str | None = None,
    **kwargs: Any,
) -> Any:
    """Write a python object to S3, encoded as JSON."""
    s3 = client("s3", sess=sess, profile=profile, region=region)
    body = json.dumps(data).encode("utf-8")
    return s3.put_object(Bucket=bucket, Key=key, Body=body, ContentType="application/json", **kwargs)
