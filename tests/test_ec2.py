""" tests for ccaaws.ec2
"""
import os

from moto import mock_ec2
import pytest

from ccaaws.ec2 import EC2


@pytest.fixture(scope="function")
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"


# @pytest.fixture
# def ec2object():
#     return EC2()
#


@mock_ec2
def test_findExistingInstance(aws_credentials):
    # secadmin-prod sectools-prod-bastion
    iid = "i-0e0529a38e748906f"
    ec2 = EC2()
    insts = ec2.findInstances([iid])
    assert len(insts) == 0


@mock_ec2
def test_findExistingInstances(aws_credentials):
    # secadmin-prod sectools-prod-bastion
    iids = ["i-0e0529a38e748906f", "i-08c2d230b11860b70"]
    ec2 = EC2()
    insts = ec2.findInstances(iids)
    assert len(insts) == 0


@mock_ec2
def test_findNonExistantInstance(aws_credentials):
    iids = ["i-33333333333333333", "i-44444444444444444"]
    ec2 = EC2()
    insts = ec2.findInstances(iids)
    assert len(insts) == 0
