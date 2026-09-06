"""Helpers for creating boto3 sessions and clients."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

import boto3


def session(
    profile: str | None = None,
    region: str | None = None,
) -> boto3.Session:
    """Create a new boto3 session, optionally using a named CLI profile and region."""
    return boto3.Session(profile_name=profile, region_name=region)


def client(
    service_name: str,
    sess: boto3.Session | None = None,
    profile: str | None = None,
    region: str | None = None,
    **kwargs: Any,
) -> Any:
    """Create a client for the given AWS service, using an existing session if provided."""
    sess = sess or session(profile=profile, region=region)
    return sess.client(service_name, **kwargs)


def assumeRoleSession(
    role_arn: str,
    role_session_name: str,
    sess: boto3.Session | None = None,
    profile: str | None = None,
    region: str | None = None,
    duration_seconds: int = 3600,
) -> boto3.Session:
    """Create a new boto3 session using temporary assumed-role credentials.

    Use this instead of `assumeRoleClient` when many different clients need
    to be created from the same assumed role.
    """
    sess = sess or session(profile=profile, region=region)
    sts = sess.client("sts")
    creds = sts.assume_role(
        RoleArn=role_arn,
        RoleSessionName=role_session_name,
        DurationSeconds=duration_seconds,
    )["Credentials"]
    return boto3.Session(
        aws_access_key_id=creds["AccessKeyId"],
        aws_secret_access_key=creds["SecretAccessKey"],
        aws_session_token=creds["SessionToken"],
        region_name=region or sess.region_name,
    )


def assumeRoleClient(
    service_name: str,
    role_arn: str,
    role_session_name: str,
    sess: boto3.Session | None = None,
    profile: str | None = None,
    region: str | None = None,
    duration_seconds: int = 3600,
    **kwargs: Any,
) -> Any:
    """Create a client for the given AWS service using temporary assumed-role credentials."""
    assumedSession = assumeRoleSession(
        role_arn,
        role_session_name,
        sess=sess,
        profile=profile,
        region=region,
        duration_seconds=duration_seconds,
    )
    return assumedSession.client(service_name, **kwargs)


def getAccountId(
    sess: boto3.Session | None = None,
    profile: str | None = None,
    region: str | None = None,
) -> str:
    """Get the AWS account id for the current (or given/assumed) session's credentials."""
    sess = sess or session(profile=profile, region=region)
    sts = sess.client("sts")
    return sts.get_caller_identity()["Account"]


def paginate(client: Any, operationName: str, resultKey: str, **kwargs: Any) -> Iterator[Any]:
    """Yield each item in `resultKey` across all pages of a paginated client call."""
    paginator = client.get_paginator(operationName)
    for page in paginator.paginate(**kwargs):
        yield from page.get(resultKey, [])

