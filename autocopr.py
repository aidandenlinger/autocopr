# Update step:
#    - if version is NOT the same, update file, make commit with tag

# Upload step
#    - if no one has updated, exit
#    - if updates have happened, push

# then on COPR side, it sees commits with that package, rebuilds, done :0

import subprocess
import re
import requests
import urllib.parse
from pathlib import Path
from dataclasses import dataclass


# From https://github.com/bkircher/python-rpm-spec, thanks!
name_pat = re.compile(r"^Name\s*:\s*(\S+)", re.IGNORECASE)
version_pat = re.compile(r"^Version\s*:\s*(\S+)", re.IGNORECASE)
url_pat = re.compile(r"^URL\s*:\s*(\S+)", re.IGNORECASE)
release_pat = re.compile(r"^Release\s*:\s*(\S+)", re.IGNORECASE)


@dataclass(frozen=True)
class SpecData:
    name: str
    version: str
    url: str
    loc: Path


def parse_spec(spec_loc: Path) -> SpecData:
    """Given a path to a Spec file, returns a parsed version and url."""
    name = None
    version = None
    url = None

    with open(spec_loc) as spec:
        for line in spec:
            # Assumes Version and URL are only defined once in the file!
            # If there are duplicate definitions, behavior is undefined!
            if (name_match := re.search(name_pat, line)) is not None:
                name = name_match.group(1)
            elif (ver_match := re.search(version_pat, line)) is not None:
                version = ver_match.group(1)
            elif (url_match := re.search(url_pat, line)) is not None:
                url = url_match.group(1)

            if name is not None and version is not None and url is not None:
                return SpecData(name, version, url, spec_loc)

    raise Exception(f"Missing version or URL in {spec_loc}!")


def is_latest_version(spec: SpecData) -> tuple[bool, str]:
    """Given SpecData, returns a pair of a boolean if
    the spec is up to date, and the latest version."""

    project_info = urllib.parse.urlparse(spec.url).path[1:]

    latest_tag: str = requests.get(
        f"https://api.github.com/repos/{project_info}/releases/latest",
        {"X-GitHub-Api-Version": "2022-11-28", "Accept": "application/vnd.github+json"},
    ).json()["tag_name"]

    # Trims tags like "v0.35.2" to "0.35.2" by cutting from the front until we
    # hit a digit
    # If your project's tags aren't as simple, this will need to be edited
    # RPM versions don't start with letters
    # Assumes the version has a digit somewhere in it
    first_digit = [x.isdigit() for x in latest_tag].index(True)
    latest_version = latest_tag[first_digit:]

    return (latest_version == spec.version, latest_version)


def update_version(spec: SpecData, latest: str):
    """Given the location of a spec file, the latest version, and the name of
    the package, update the version in the spec and make a commit with the
    cooresponding COPR tag."""

    spec_loc_backup = spec.loc.rename(spec.loc.with_suffix(spec.loc.suffix + ".bak"))

    with (open(spec.loc, "w") as new_spec, open(spec_loc_backup) as old_spec):
        for line in old_spec:
            if re.match(version_pat, line):
                new_spec.write(f"Version: {latest}\n")
            elif re.match(release_pat, line):
                # All new versions must start at release 1
                new_spec.write("Release: 1%{dist}\n")
            else:
                new_spec.write(line)

    spec_loc_backup.unlink()

    # Add a commit with this update and tag it so COPR sees it
    subprocess.run(["git", "add", str(spec.loc)])
    subprocess.run(["git", "commit", "-m", f"Updated {spec.name} to {latest}"])
    subprocess.run(["git", "tag", f"{spec.name}-{latest}"])


def main():
    any_updated = False

    for spec_loc in Path("specs").glob("*.spec"):
        spec = parse_spec(spec_loc)
        is_latest, latest = is_latest_version(spec)

        # Track if any have an update
        any_updated = any_updated | is_latest

        if not is_latest:
            update_version(spec, latest)

        # add to log

    # print log status

    # if any_updated and push flag handed in:
    #    git push
    # else:
    #    print message that commits are ready


if __name__ == "__main__":
    main()
