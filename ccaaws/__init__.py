""" ccaaws package

package __version__ variable is set from the pyproject.toml file
version key.
"""

import os

__version__ = "0.0.0"

# obtain version information from the pyproject.toml file
# which is in the directory hierarchy somewhere above this file
dird = os.path.dirname(__file__)
while dird != "/" or dird != "":
    pfn = os.path.join(dird, "pyproject.toml")
    if os.path.exists(pfn):
        with open(pfn, "r") as f:
            for line in f:
                if line.startswith("version"):
                    tmp = line.split("=")
                    vtmp = tmp[1].strip().split('"')
                    if len(vtmp) > 1:
                        __version__ = vtmp[1]
                    else:
                        __version__ = vtmp[0]
                    break
        break
    else:
        dird = os.path.dirname(dird)
