""" ccaaws package

package __version__ variable is set from the pyproject.toml file
version key.
"""

import os
import toml

__version__ = "0.0.0"

# obtain version information from the pyproject.toml file
# which is in the directory hierarchy somewhere above this file
dird = os.path.dirname(__file__)
while dird != "/" or dird != "":
    pfn = os.path.join(dird, "pyproject.toml")
    if os.path.exists(pfn):
        td = toml.load(pfn)
        __version__ = td["tool"]["poetry"]["version"]
        break
    else:
        dird = os.path.dirname(dird)
