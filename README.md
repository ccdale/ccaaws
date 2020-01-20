# ccaaws

Python objects wrapped around [boto3](https://github.com/boto/boto3)

## botosession.py

Base class inherited by all the others.  Manages connections to AWS via
access keys or profiles.

## iamclient.py

Access to IAM functions - mainly for user access key management.

```
from ccaaws.iamclient import IamClient

iam = IamClient("iam.user")
newkeys = iam.rotateKeys()
```

[modeline]: # ( vim: set ft=markdown tw=74 fenc=utf-8 spell spl=en_gb mousemodel=popup: )
