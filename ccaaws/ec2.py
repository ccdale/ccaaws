""" ccaaws ec2 class
"""
import sys
from ccaaws import __version__
from ccaaws.botosession import BotoSession
from ccautils.errors import errorRaise
from botocore.exceptions import ClientError
import ccalogging

log = ccalogging.log


class EC2(BotoSession):
    def __init__(self, **kwargs):
        """ connect to aws

        to switch region supply the `region` keyword
        """
        super().__init__(**kwargs)
        self.newClient("ec2")

    def findInstances(self, instlist):
        """ find instances in instlist

        instlist is a list of instance-id strings
        """
        try:
            instances = []
            kwargs = {}
            kwargs["InstanceIds"] = instlist
            while True:
                try:
                    # will raise client error if instances don't exist
                    resp = self.client.describe_instances(**kwargs)
                    try:
                        if "Reservations" in resp:
                            for r in resp["Reservations"]:
                                if "Instances" in r:
                                    for i in r["Instances"]:
                                        instances.append(i)
                        kwargs["NextToken"] = resp["NextToken"]
                    except KeyError:
                        break
                except ClientError as ce:
                    log.debug(f"ClientError: Instances probably don't exist: {ce}")
                    break
            return instances
        except Exception as e:
            fname = sys._getframe().f_code.co_name
            errorRaise(fname, e)

    def getMatchingInstances(self, instlst=None):
        """ find the instances named in the `instlst` list
        or all instances if `instlst` is None

        NOTE: this does not appear to work with filters, use
        the 'findInstances' function above
        """
        try:
            instances = []
            kwargs = {}
            if type(instlst) is list:
                kwargs["Filters"] = [{"Name": "instance-id", "Values": instlst,}]
            while True:
                resp = self.client.describe_instances(**kwargs)
                try:
                    if "Reservations" in resp:
                        for r in resp["Reservations"]:
                            if "Instances" in r:
                                for i in r["Instances"]:
                                    instances.append(i)
                    kwargs["NextToken"] = resp["NextToken"]
                except KeyError:
                    break
            return instances
        except Exception as e:
            fname = sys._getframe().f_code.co_name
            errorRaise(fname, e)

    def getRegions(self):
        """
        returns a list of all available regions
        """
        try:
            regions = []
            resp = self.client.describe_regions()
            if "Regions" in resp:
                for region in resp["Regions"]:
                    regions.append(region["RegionName"])
            log.debug("Regions: {}".format(regions))
            return regions
        except Exception as e:
            fname = sys._getframe().f_code.co_name
            errorRaise(fname, e)
