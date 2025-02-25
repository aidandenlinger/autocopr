#!/bin/env python3
from collections import namedtuple

from copr.v3 import Client
from packages import thirdparty_packages_dict

thirdparty_pkgs_array = thirdparty_packages_dict()["packages"]

# COPR API Client
client = Client.create_from_config_file()

# Define the namedtuple
Package = namedtuple("Git_package", ["name", "source_dict"])

# Convert the dictionary to an array of namedtuples
thirdparty_pkgs_array = [
    Package(name=pkg["name"], source_dict=pkg["source_dict"])
    for pkg in thirdparty_packages_dict()["packages"]
]

# Print all variables from the namedtuple
for pkg in thirdparty_pkgs_array:
    name = pkg.name
    source_dict = pkg.source_dict
    clone_url = pkg.source_dict["clone_url"]
    subdirectory = pkg.source_dict["subdirectory"]
    specfile = pkg.source_dict["spec"]
    source_build_method = pkg.source_dict["source_build_method"]
    print(
        f"Name: {name}",
        f"Clone URL: {clone_url}",
        f"Subdirectory: {subdirectory}",
        f"Specfile: {specfile}",
        f"Source Build Method: {source_build_method}",
        "----------------",
        sep="\n",
    )
    client.package_proxy.edit(
        "relativesure",  # owner name
        "all-packages",  # project name
        name,  # package name
        "scm",  # source type
        {
            "clone_url": clone_url,
            "subdirectory": subdirectory,
            "spec": specfile,
            "scm_type": "git",
            "source_build_method": source_build_method,
        },  # source dict
    )
