# ccaaws

A small `uv`-managed Python library for creating boto3 sessions and clients,
including assumed-role clients.

Requires Python >= 3.14.

## Install

```bash
uv add ccaaws
```

## Usage

```python
import ccaaws

# a plain boto3 session, optionally with a named CLI profile and/or region
sess = ccaaws.session(profile="myprofile", region="eu-west-1")

# a client for any AWS service, reusing a session if one is given
s3 = ccaaws.client("s3", sess=sess)

# or let it create its own session
ec2 = ccaaws.client("ec2", profile="myprofile", region="eu-west-1")

# a client built from temporary assumed-role credentials
sts_client = ccaaws.assumeRoleClient(
    "s3",
    "arn:aws:iam::123456789012:role/myrole",
    "mysession",
    profile="myprofile",
    region="eu-west-1",
)
```

## API

- `session(profile=None, region=None) -> boto3.Session`
  Creates a new boto3 session, optionally using a named CLI profile and/or region.

- `client(service_name, sess=None, profile=None, region=None, **kwargs) -> Any`
  Creates a client for the given AWS service, reusing `sess` if provided,
  otherwise creating a new session from `profile`/`region`. Extra `kwargs`
  are passed through to `Session.client()`.

- `assumeRoleClient(service_name, role_arn, role_session_name, sess=None, profile=None, region=None, duration_seconds=3600, **kwargs) -> Any`
  Calls STS `AssumeRole` for `role_arn` and returns a client for `service_name`
  built from the resulting temporary credentials. Extra `kwargs` are passed
  through to `Session.client()`.

## Development

```bash
uv sync
uv run pytest
```
