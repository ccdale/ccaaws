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

# a session built from temporary assumed-role credentials, for creating
# many different clients from the same assumed role
assumedSess = ccaaws.assumeRoleSession(
    "arn:aws:iam::123456789012:role/myrole",
    "mysession",
)
s3 = ccaaws.client("s3", sess=assumedSess)
ec2 = ccaaws.client("ec2", sess=assumedSess)

# which AWS account the current (or assumed) session's credentials belong to
accountId = ccaaws.getAccountId(sess=assumedSess)

# read a parameter (or SecureString secret) from SSM Parameter Store
value = ccaaws.getParameter("/my/param")

# read a secret from Secrets Manager
secret = ccaaws.getSecret("mySecretId")

# read/write a python dict as a JSON object in S3
data = ccaaws.s3GetJson("mybucket", "mykey.json")
ccaaws.s3PutJson("mybucket", "mykey.json", data)

# yield every item across all pages of a paginated client call
for bucket in ccaaws.paginate(s3, "list_buckets", "Buckets"):
    print(bucket["Name"])
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

- `assumeRoleSession(role_arn, role_session_name, sess=None, profile=None, region=None, duration_seconds=3600) -> boto3.Session`
  Calls STS `AssumeRole` for `role_arn` and returns a `boto3.Session` built
  from the resulting temporary credentials. Use this instead of
  `assumeRoleClient` when many different clients need to be created from the
  same assumed role.

- `getAccountId(sess=None, profile=None, region=None) -> str`
  Returns the AWS account id that the given (or newly created) session's
  credentials belong to. Useful when working with multiple assumed roles
  to know which account you are currently in.

- `getParameter(name, sess=None, profile=None, region=None, withDecryption=True, **kwargs) -> str`
  Reads a parameter (including `SecureString` secrets) from SSM Parameter
  Store and returns its value.

- `getSecret(secretId, sess=None, profile=None, region=None, **kwargs) -> str`
  Reads a secret value from AWS Secrets Manager.

- `s3GetJson(bucket, key, sess=None, profile=None, region=None, **kwargs) -> Any`
  Reads an S3 object and parses its body as JSON, returning a python object
  (typically a `dict`).

- `s3PutJson(bucket, key, data, sess=None, profile=None, region=None, **kwargs) -> Any`
  Writes a python object to S3, encoded as JSON.

- `paginate(client, operationName, resultKey, **kwargs) -> Iterator[Any]`
  Universal pagination helper: yields every item under `resultKey` across
  all pages of the paginated `operationName` call on `client`, passing
  `kwargs` through to `paginate()`.

## Thread safety (AWS Lambda usage)

boto3 sessions are **not** thread-safe: a `boto3.Session` (and anything created
from it, like credential resolution state) must not be shared across threads.
boto3 clients created from a session, however, **are** thread-safe and can be
shared and reused across threads once created.

This matters for Lambda functions that use threads (for example, to fan out
concurrent I/O within a single invocation): create one `session()` per thread,
but a `client()` built from that session can be handed to, or shared with,
other threads that need to call the same service.

Recommended patterns for Lambda:

- **Single-threaded handler (the common case)**: create the session and
  client(s) once at module scope, outside the handler function, so they are
  reused across warm invocations of the same execution environment.

  ```python
  import ccaaws

  # module scope - created once per execution environment, reused across
  # warm invocations
  s3 = ccaaws.client("s3")

  def handler(event, context):
      return s3.list_buckets()
  ```

- **Multi-threaded handler**: create a separate `session()` per thread (for
  example, in the thread's target function or via thread-local storage).
  Clients built from those sessions can then be shared across threads if
  needed, since clients are thread-safe.

  ```python
  import threading

  import ccaaws

  threadLocal = threading.local()


  def getClient():
      if not hasattr(threadLocal, "s3"):
          sess = ccaaws.session()
          threadLocal.s3 = ccaaws.client("s3", sess=sess)
      return threadLocal.s3
  ```

- **`concurrent.futures.ThreadPoolExecutor`**: the cleaner, more modern way
  to fan out work across threads. Since a worker function may run on any
  thread in the pool, each call must create its own `session()`; `threading`
  primitives (locks, thread-local storage) are still useful when workers need
  to share or protect other state.

  ```python
  from concurrent.futures import ThreadPoolExecutor

  import ccaaws


  def fetchBucketTags(bucketName: str) -> dict:
      # one session per call, since this runs on a pool thread
      s3 = ccaaws.client("s3", sess=ccaaws.session())
      return s3.get_bucket_tagging(Bucket=bucketName)


  def handler(event, context):
      bucketNames = event["bucketNames"]
      with ThreadPoolExecutor(max_workers=len(bucketNames)) as pool:
          return list(pool.map(fetchBucketTags, bucketNames))
  ```

Do not store a `session()` on a module-level variable and then use it from
multiple threads; create one session per thread instead.

## Development

```bash
uv sync
uv run pytest
```
