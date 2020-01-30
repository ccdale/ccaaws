import os
import ccalogging
from ccaaws.errors import errorRaise

log = ccalogging.log


def readFile(fqfn):
    try:
        op = None
        if os.path.exists(fqfn):
            with open(fqfn, "r") as ifn:
                lines = ifn.readlines()
            for line in lines:
                if op is None:
                    op = line
                else:
                    op += line
        return op
    except Exception as e:
        fname = sys._getframe().f_code.co_name
        errorRaise(fname, e)


def makeDictFromString(istr):
    """ makes a dictionary from a string of parameters

    leading and trailing white space is stripped

    params:
        istr: a string in the form:
            'someparam= somevalue,someotherparam =someothervalue  '

    returns a dictionary:
        {"someparam": "somevalue", "someotherparam": "someothervalue"}
    """
    try:
        pd = {}
        if "=" in strparams:
            ea = strparams.split(",")
            for p in ea:
                tmp = p.split("=")
                pd[tmp[0].strip()] = tmp[1].strip()
        return pd
    except Exception as e:
        fname = sys._getframe().f_code.co_name
        errorRaise(fname, e)
