import sys
import time
from ccaaws.botosession import BotoSession
from ccaaws.errors import errorRaise
from botocore.exceptions import ClientError
import ccalogging
import ccaaws.utils as UT

log = ccalogging.log


class CFNClient(BotoSession):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.newClient("cloudformation")

    def stackDetails(self, stackname):
        try:
            resp = self.client.describe_stacks(StackName=stackname)
            if "Stacks" in resp:
                stack = resp["Stacks"][0]
                return stack
        except ClientError as ce:
            log.debug(f"stack: {stackname} does not exist")
            return None
        except Exception as e:
            fname = sys._getframe().f_code.co_name
            errorRaise(fname, e)

    def stackStatus(self, stackname):
        try:
            stack = self.stackDetails(stackname)
            return stack["StackStatus"] if stack is not None else None
        except Exception as e:
            fname = sys._getframe().f_code.co_name
            errorRaise(fname, e)

    def createStack(self, **kwargs):
        try:
            resp = self.client.create_stack(**kwargs)
            if "StackId" in resp:
                return resp["StackId"]
            return None
        except Exception as e:
            fname = sys._getframe().f_code.co_name
            errorRaise(fname, e)

    def updateStack(self, **kwargs):
        try:
            resp = self.client.update_stack(**kwargs)
            if "StackId" in resp:
                return resp["StackId"]
            return None
        except Exception as e:
            fname = sys._getframe().f_code.co_name
            errorRaise(fname, e)

    def deleteStack(self, stackname):
        try:
            self.client.delete_stack(StackName=stackname)
        except Exception as e:
            fname = sys._getframe().f_code.co_name
            errorRaise(fname, e)

    def waitForStack(self, stackn, timeout=10, sleeptime=30):
        """ wait for a stack to become "..._COMPLETE"

        waits for timeout * sleeptime seconds

        returns the stack status
        """
        try:
            status = None
            cn = 0
            sleeptime = sleeptime
            while True:
                cn += 1
                if cn > timeout:
                    log.error(
                        f"Timeout expired waiting for stack {stackn} to become ready"
                    )
                    break
                status = self.stackStatus(stackn)
                if status is not None and "COMPLETE" in status:
                    log.info(f"Stack {stackn} is {status}")
                    break
                elif status is None:
                    log.warning(f"stack {stackn} does not exist (anymore)")
                    break
                time.sleep(sleeptime)
            return status
        except Exception as e:
            fname = sys._getframe().f_code.co_name
            errorRaise(fname, e)

    def expandDictToList(self, xdict, keyname="Key", valuename="Value"):
        """ expands a dictionary into a list of dictionaries, one per key

            {"somekey": "someval", "otherkey": "otherval"}

        returns a list of dictionaries

            [
                {"Key": "somekey", "Value": "someval"},
                {"Key": "otherkey", "Value": "otherval"},
            ]
        """
        try:
            op = []
            for key in xdict:
                tmp = {keyname: key, valuename: xdict[key]}
                op.append(tmp)
            return op
        except Exception as e:
            fname = sys._getframe().f_code.co_name
            errorRaise(fname, e)

    def buildStackTags(self, tagdict):
        """ converts a set of tags into the form used by CFN Stacks

                tagdict = {
                    "owner": "sre",
                    "environment": "prod",
                    "product": "ccaaws",
                    "version": __version__,
                }

        returns a list of dictionaries
            [
                {"Key": "owner", "Value": "sre"},
                {"Key": "environment", "Value": "prod"},
                {"Key": "product", "Value": "ccaaws"},
                {"Key": "version", "Value": __version__},
            ]
        """
        try:
            return self.expandDictToList(tagdict)
        except Exception as e:
            fname = sys._getframe().f_code.co_name
            errorRaise(fname, e)

    def buildStackParams(self, paramstr):
        """ builds a set of parameters from a paramstring
        """
        try:
            pd = self.makeParamDict(paramstr)
            lpd = self.expandDictToList(
                pd, keyname="ParameterKey", valuename="ParameterValue"
            )
            return lpd
        except Exception as e:
            fname = sys._getframe().f_code.co_name
            errorRaise(fname, e)

    def makeParamDictFromString(self, strparams):
        """ makes a dictionary from a string of parameters

        params:
          strparams: a string in the form:
                'someparam=somevalue,someotherparam=someothervalue'

        returns a dictionary:
           {"someparam": somevalue, "someotherparam": someothervalue}
        """
        try:
            return UT.makeDictFromString(strparams)
        except Exception as e:
            fname = sys._getframe().f_code.co_name
            errorRaise(fname, e)

    def getTemplate(self, fqfn):
        try:
            return UT.readFile(fqfn)
        except Exception as e:
            fname = sys._getframe().f_code.co_name
            errorRaise(fname, e)
