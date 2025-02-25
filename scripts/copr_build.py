#!/bin/env python3
import sys

from copr.v3 import Client

# COPR API Client
client = Client.create_from_config_file()

# Split package list with comma
pkg_list = sys.argv[1].split(",")
print("Running builds for:")
print(pkg_list)

for pkg in pkg_list:
    client.package_proxy.build(
        "relativesure",  # owner name
        "all-packages",  # project name
        pkg,  # package name
    )
