"""Helpers for reading parameters from SSM Parameter Store."""

from __future__ import annotations

from typing import Any

import boto3

from ccaaws.session import client


def getParameter(
    name: str,
    sess: boto3.Session | None = None,
    profile: str | None = None,
    region: str | None = None,
    withDecryption: bool = True,
    **kwargs: Any,
) -> str:
    """Read a parameter (or SecureString secret) from SSM Parameter Store."""
    ssm = client("ssm", sess=sess, profile=profile, region=region)
    resp = ssm.get_parameter(Name=name, WithDecryption=withDecryption, **kwargs)
    return resp["Parameter"]["Value"]
