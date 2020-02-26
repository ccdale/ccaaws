"""AWS Dynamo DB table awsaccounts"""
# vim: set expandtab tabstop=4 shiftwidth=4 softtabstop=4 foldmethod=indent:

import ccalogging

from ccaaws.dynamo import DynamoDB

log = ccalogging.log


class AWSAccounts(DynamoDB):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def getAccountID(self, accountname):
        accountnumber = None
        item = {
            "TableName": "awsaccounts",
            "Key": {"accountname": {"S": accountname,},},
        }
        resp = self.getItem(item)
        if resp is not None:
            if "Item" in resp:
                if "accountnumber" in resp["Item"]:
                    if "S" in resp["Item"]["accountnumber"]:
                        try:
                            accountnumber = resp["Item"]["accountnumber"]["S"]
                        except Exception as e:
                            log.info(
                                "Failed to retrieve account number for {}, response was {}, exception was {}".format(
                                    accountname, resp, e
                                )
                            )
                    else:
                        log.info(
                            "Account number is not a string for {}, response was {}".format(
                                accountname, resp
                            )
                        )
        return accountnumber

    def findAccountNumber(self, acctname):
        """finds the account number regardless of case"""
        ret = self.getAccountID(acctname)
        if ret is None:
            data = self.getAllAccounts()
            for datum in data:
                if datum["accountname"].lower() == acctname.lower():
                    ret = datum["accountnumber"]
                    break
        return ret

    def findAccountName(self, accountnumber):
        ret = None
        data = self.getAllAccounts()
        for datum in data:
            if datum["accountnumber"] == accountnumber:
                ret = datum["accountname"]
                break
        return ret

    def setAccountID(self, accountname, accountnumber):
        ret = False
        item = {
            "TableName": "awsaccounts",
            "Item": {
                "accountname": {"S": accountname,},
                "accountnumber": {"S": accountnumber,},
            },
        }
        try:
            resp = self.putItem(item)
            ret = True
        except Exception as e:
            log.warning(
                "exception when putting item {}, response was {}, exception was {}".format(
                    item, resp, e
                )
            )
        return ret

    def getAllAccounts(self):
        items = self.getAll("awsaccounts")
        data = []
        for item in items:
            data.append(
                {
                    "accountname": item["accountname"]["S"],
                    "accountnumber": item["accountnumber"]["S"],
                }
            )
        return data

    def deleteAccount(self, accountname):
        ret = False
        item = {
            "TableName": "awsaccounts",
            "Key": {"accountname": {"S": accountname,},},
        }
        try:
            self.deleteItem(item)
            ret = True
        except Exception as e:
            log.warning("Failure deleting {}".format(accountname))
        return ret
