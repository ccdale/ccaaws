"""
errors module for ccaaws module
"""
import sys


def formatErrorMsg(funcname, exc):
    ename = type(exc).__name__
    return f"Error in {funcname}: {ename}: {exc}\n"


def errorExit(funcname, exc, errorvalue=1):
    sys.stderr.write(formatErrorMsg(funcname, exc))
    sys.exit(errorvalue)


def errorRaise(funcname, exc):
    sys.stderr.write(formatErrorMsg(funcname, exc))
    raise (exc)


def errorNotify(funcname, exc):
    sys.stderr.write(formatErrorMsg(funcname, exc))
