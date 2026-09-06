"""Helpers for reading secrets from AWS Secrets Manager."""

from __future__ import annotations

from typing import Any

import boto3

from ccaaws.session import client


def getSecret(
    secretId: str,
    sess: boto3.Session | None = None,
    profile: str | None = None,
    region: str | None = None,
    **kwargs: Any,
) -> str:
    """Read a secret value from AWS Secrets Manager."""
    sm = client("secretsmanager", sess=sess, profile=profile, region=region)
    resp = sm.get_secret_value(SecretId=secretId, **kwargs)
    if "SecretString" in resp:
        return resp["SecretString"]
    # boto3 already base64-decodes SecretBinary into raw bytes
    return resp["SecretBinary"].decode("utf-8")

