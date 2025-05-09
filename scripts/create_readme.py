#!/bin/env python3
import pathlib
from collections import namedtuple

from packages import packagelist, thirdparty_packages_dict

package_array = packagelist()
thirdparty_package_array = []

# Define the namedtuple
Package = namedtuple("Git_package", ["name", "source_dict"])

# Convert the dictionary to an array of namedtuples
thirdparty_pkgs_array = [
    Package(name=pkg["name"], source_dict=pkg["source_dict"])
    for pkg in thirdparty_packages_dict()["packages"]
]

for pkg in thirdparty_pkgs_array:
    name = pkg.name
    url = pkg.source_dict["clone_url"]
    print(name)
    print(url)
    if name and url:
        thirdparty_package_array.append((name, url))

# Create markdown content for README.md
readme_content = """# Autocopr forked repo

![CodeRabbit Pull Request Reviews](https://img.shields.io/coderabbit/prs/github/RelativeSure/autocopr?utm_source=oss&utm_medium=github&utm_campaign=RelativeSure%2Fautocopr&labelColor=171717&color=FF570A&link=https%3A%2F%2Fcoderabbit.ai&label=CodeRabbit+Reviews&style=for-the-badge)
![CircleCI](https://img.shields.io/circleci/build/github/RelativeSure/autocopr?style=for-the-badge&label=CircleCI)

## Description

This COPR repo is for personal and work use. Please go ahead and use this copr repo, be aware that the repo might be abandoned at any point. Feel free to create a GitHub issue if there's any issues with packages.

## List of packages from `specs/` folder

### Status badges on COPR builds
"""

for name, url, version in package_array:
    readme_content += f"""
### [{name}](specs/{name}.spec) v{version}

[Upstream]({url})

![{name} status](https://copr.fedorainfracloud.org/coprs/relativesure/all-packages/package/{name}/status_image/last_build.png)
"""

readme_content += """
## Following packages are from thirdparty sources

> [!WARNING]
> The list below contains packages from thirdparty sources.
"""

for name, url in thirdparty_package_array:
    readme_content += f"""
### {name}

![{name} status](https://copr.fedorainfracloud.org/coprs/relativesure/all-packages/package/{name}/status_image/last_build.png)

[Upstream]({url})
"""

# Write markdown content to README.md
readme_path = pathlib.Path("README.md")
with readme_path.open("w", encoding="utf-8") as readme_file:
    readme_file.write(readme_content)

print("README.md file created successfully!")
