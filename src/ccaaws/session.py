"""Helpers for creating boto3 sessions and clients."""

from __future__ import annotations

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
    sess = sess or session(profile=profile, region=region)
    sts = sess.client("sts")
    creds = sts.assume_role(
        RoleArn=role_arn,
        RoleSessionName=role_session_name,
        DurationSeconds=duration_seconds,
    )["Credentials"]
    assumed_session = boto3.Session(
        aws_access_key_id=creds["AccessKeyId"],
        aws_secret_access_key=creds["SecretAccessKey"],
        aws_session_token=creds["SessionToken"],
        region_name=region or sess.region_name,
    )
    return assumed_session.client(service_name, **kwargs)
