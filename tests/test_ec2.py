""" tests for ccaaws.ec2
"""
from ccaaws.ec2 import EC2


def test_findExistingInstance():
    # secadmin-prod sectools-prod-bastion
    iid = "i-0e0529a38e748906f"
    ec = EC2()
    insts = ec.findInstances([iid])
    assert len(insts) == 1


def test_findExistingInstances():
    # secadmin-prod sectools-prod-bastion
    iids = ["i-0e0529a38e748906f", "i-08c2d230b11860b70"]
    ec = EC2()
    insts = ec.findInstances(iids)
    assert len(insts) == 2


def test_findNonExistantInstance():
    iids = ["i-33333333333333333", "i-44444444444444444"]
    ec = EC2()
    insts = ec.findInstances(iids)
    assert len(insts) == 0
