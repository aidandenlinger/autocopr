#!/bin/env python3
from collections import namedtuple

from copr.v3 import Client
from packages import thirdparty_packages_dict

# COPR API Client
client = Client.create_from_config_file("copr")


def main():
    # Define the namedtuple
    Package = namedtuple("Git_package", ["name", "source_dict"])

    # Convert the dictionary to an array of namedtuples
    thirdparty_pkgs_array = [
        Package(name=pkg["name"], source_dict=pkg["source_dict"])
        for pkg in thirdparty_packages_dict()["packages"]
    ]

    for pkg in thirdparty_pkgs_array:
        print(f"Updating package {pkg.name}")
        build_packages(pkg.name)


def build_packages(pkgName):
    client.package_proxy.build(
        "relativesure", "all-packages", pkgName, buildopts={"background": True}
    )


if __name__ == "__main__":
    main()
