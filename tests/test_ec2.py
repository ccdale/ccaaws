""" tests for ccaaws.ec2
"""
import pytest

from moto import moto_ec2

from ccaaws.ec2 import EC2


@pytest.fixture
def ec2object():
    return EC2()


@moto_ec2
def test_findExistingInstance(ec2object):
    # secadmin-prod sectools-prod-bastion
    iid = "i-0e0529a38e748906f"
    insts = ec2object.findInstances([iid])
    assert len(insts) == 1


@moto_ec2
def test_findExistingInstances(ec2object):
    # secadmin-prod sectools-prod-bastion
    iids = ["i-0e0529a38e748906f", "i-08c2d230b11860b70"]
    insts = ec2object.findInstances(iids)
    assert len(insts) == 2


@moto_ec2
def test_findNonExistantInstance(ec2object):
    iids = ["i-33333333333333333", "i-44444444444444444"]
    insts = ec2object.findInstances(iids)
    assert len(insts) == 0
