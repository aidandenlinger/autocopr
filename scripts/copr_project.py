#!/bin/env python3
from collections import namedtuple

from copr.v3 import Client
from packages import packagelist, thirdparty_packages_dict

# COPR API Client
client = Client.create_from_config_file()


def thirdparty_pkgs():
    # Define the namedtuple
    Package = namedtuple("Git_package", ["name", "source_dict"])
    package_list = []

    # Convert the dictionary to an array of namedtuples
    thirdparty_pkgs_array = [
        Package(name=pkg["name"], source_dict=pkg["source_dict"])
        for pkg in thirdparty_packages_dict()["packages"]
    ]

    for pkg in thirdparty_pkgs_array:
        package_list.append(pkg.name)
    return package_list


def main():
    package_array = packagelist()

    # List of fedora versions
    fedora_version_list = ["fedora-40-x86_64", "fedora-41-x86_64"]
    fedora_rawhide_version_list = [
        "fedora-40-x86_64",
        "fedora-41-x86_64",
        "fedora-rawhide-x86_64",
    ]

    # List of thirdparty packages
    # thirdparty_package_array = ["rust-tealdeer", "wezterm", "zed", "zed-preview"]
    thirdparty_package_array = thirdparty_pkgs()

    # Description
    readme_content = """This COPR repo is for personal and work use.

Please go ahead and use this copr repo, be aware that the repo might be abandoned at any point.

Feel free to create a GitHub issue if there's any issues with the packages.

The following packages are installed from a 3rd party source than autocopr github repo.

"""

    for thirdparty_package in thirdparty_package_array:
        readme_content += f"**`{thirdparty_package}`**\n"

    readme_content += (
        "### **List of packages from relativesure/autocopr github repos**\n"
    )

    for name, url, version in package_array:
        print(f"Name: {name} URL: {url} Version: {version}")
        readme_content += f"**`{name}`** ( [Upstream]({url}) )\n\n"

    # Instructions
    instructions_content = """### **Enable COPR repo**
$`sudo dnf copr enable relativesure/all-packages`


### **Install all packages**
$`sudo dnf install"""
    for name, url, version in package_array:
        print(f"Name: {name} URL: {url} Version: {version}")
        instructions_content += f" {name}"

    for thirdparty_package in thirdparty_package_array:
        instructions_content += f" {thirdparty_package}"

    instructions_content += "`"

    # Setup copr repo
    client.project_proxy.edit(
        "relativesure",  # ownername
        "all-packages",  # projectname
        fedora_rawhide_version_list,  # chroots
        description=readme_content,
        instructions=instructions_content,
        homepage="https://github.com/RelativeSure/autocopr",
        unlisted_on_hp=False,
        enable_net=True,
        follow_fedora_branching=True,
    )

    # Add additional_repos for fedora released versions
    for chroot_name in fedora_version_list:
        client.project_chroot_proxy.edit(
            "relativesure",  # ownername
            "all-packages",  # projectname
            chroot_name,  # chroots without rawhide
            additional_repos="https://repos.fyralabs.com/terra$releasever/",
        )


if __name__ == "__main__":
    main()
