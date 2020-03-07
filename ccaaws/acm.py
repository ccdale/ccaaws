import sys
import ccautils.util as UT
from acmtool.botosession import BotoSession
from acmtool.errors import errorRaise


class ACM(BotoSession):
    def __init__(self, **kwargs):
        try:
            super().__init__(**kwargs)
            self.newClient("acm")
        except Exception as e:
            fname = sys._getframe().f_code.co_name
            errorRaise(fname, e)

    def getCertList(self):
        try:
            pag = self.client.get_paginator("list_certificates")
            pageit = pag.paginate()
            certs = []
            for page in pageit:
                if "CertificateSummaryList" in page:
                    for cert in page["CertificateSummaryList"]:
                        certs.append(cert["CertificateArn"])
            return certs
        except Exception as e:
            fname = sys._getframe().f_code.co_name
            errorRaise(fname, e)

    def getCertDetails(self, certarn):
        try:
            cert = self.client.describe_certificate(CertificateArn=certarn)
            return cert["Certificate"]
        except Exception as e:
            fname = sys._getframe().f_code.co_name
            errorRaise(fname, e)

    def getCerts(self, emailvalidationonly=True):
        try:
            carns = self.getCertList()
            # print(carns)
            certs = []
            ecn = 0
            dcn = 0
            for arn in carns:
                cert = self.getCertDetails(arn)
                if len(cert) > 0:
                    # print("{}".format(cert))
                    tcert = {"arn": arn}
                    tcert["inuse"] = []
                    if "InUseBy" in cert:
                        tcert["inuse"] = cert["InUseBy"]
                    if "NotAfter" in cert:
                        tcert["expirests"], tcert["expires"] = UT.fuzzyExpires(
                            cert["NotAfter"]
                        )
                    else:
                        tcert["expirests"] = 0
                        tcert["expires"] = ""
                    tcert["domain"] = cert["DomainName"]
                    tcert["altdomains"] = cert["SubjectAlternativeNames"]
                    vopt = []
                    tcert["status"] = "unknown"
                    for opt in cert["DomainValidationOptions"]:
                        tcert["validation"] = opt["ValidationMethod"]
                        if tcert["validation"] == "EMAIL":
                            ecn += 1
                        else:
                            dcn += 1
                        if "ValidationStatus" in opt:
                            tcert["status"] = opt["ValidationStatus"]
                        xval = {
                            "domain": opt["DomainName"],
                            "validationdomain": opt["ValidationDomain"],
                        }
                        vopt.append(xval)
                    tcert["validations"] = vopt
                    if emailvalidationonly:
                        if tcert["validation"] == "EMAIL":
                            certs.append(tcert)
                    else:
                        certs.append(tcert)
            return (ecn, dcn, certs)
        except Exception as e:
            fname = sys._getframe().f_code.co_name
            errorRaise(fname, e)
