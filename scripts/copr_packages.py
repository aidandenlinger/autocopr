#!/bin/env python3
from copr.v3 import Client
from scripts.packages import packagelist

package_array = packagelist()

# COPR API Client
client = Client.create_from_config_file()

# COPR add packages
for name, url, version in package_array:
    client.package_proxy.edit(
        "relativesure",  # owner name
        "all-packages",  # project name
        name,  # package name
        "scm",  # source type
        {
            "clone_url": "https://github.com/RelativeSure/autocopr",
            "subdirectory": "specs",
            "spec": f"{name}.spec",
            "scm_type": "git",
            "source_build_method": "rpkg",
        },  # source dict
    )
