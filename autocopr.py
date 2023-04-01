import logging
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
    url: urllib.parse.ParseResult
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
                logging.info(f'Got name from: "{line.rstrip()}"')
                name = name_match.group(1)
            elif (ver_match := re.search(version_pat, line)) is not None:
                logging.info(f'Got version from: "{line.rstrip()}"')
                version = ver_match.group(1)
            elif (url_match := re.search(url_pat, line)) is not None:
                logging.info(f'Got url from: "{line.rstrip()}"')
                url = urllib.parse.urlparse(url_match.group(1))

            if name is not None and version is not None and url is not None:
                return SpecData(name, version, url, spec_loc)

    raise Exception(f"Missing version or URL in {spec_loc}!")


def is_latest_version(spec: SpecData) -> tuple[bool, str]:
    """Given SpecData with a github url, returns a pair of a boolean if
    the spec is up to date and the latest version."""

    project_info = spec.url.path[1:]
    url = f"https://api.github.com/repos/{project_info}/releases/latest"
    logging.info(f"Querying {url}")

    latest_tag: str = requests.get(
        url,
        {"X-GitHub-Api-Version": "2022-11-28",
            "Accept": "application/vnd.github+json"},
    ).json()["tag_name"]

    # Trims tags like "v0.35.2" to "0.35.2" by cutting from the front until we
    # hit a digit
    # If your project's tags aren't as simple, this will need to be edited
    # RPM versions don't start with letters
    # Assumes the version has a digit somewhere in it
    first_digit = [x.isdigit() for x in latest_tag].index(True)
    latest_version = latest_tag[first_digit:]

    return (latest_version == spec.version, latest_version)


def update_version(
    spec: SpecData, latest: str, inplace: bool = False, push: bool = False
):
    """Given the location of a spec file, the latest version, and the name of
    the package, update the version in the spec and make a commit with the
    cooresponding COPR tag."""

    spec_loc_backup = spec.loc.rename(
        spec.loc.with_suffix(spec.loc.suffix + ".bak"))

    with (open(spec.loc, "w") as new_spec, open(spec_loc_backup) as old_spec):
        # Again, assumes that Version and Release are only defined once!
        for line in old_spec:
            if re.match(version_pat, line):
                new_spec.write(f"Version: {latest}\n")
            elif re.match(release_pat, line):
                # Ensure we're using autorelease
                new_spec.write("Release: %autorelease\n")
            else:
                new_spec.write(line)

    if inplace:
        spec_loc_backup.unlink()

    # Add a commit with this update and tag it so COPR sees it
    if push:
        subprocess.run(["git", "add", str(spec.loc)])
        subprocess.run(
            ["git", "commit", "-m", f"Update {spec.name} to {latest}"])
        # Force the new tag, useful for testing
        # Have to make an annotated tag for github to recognize it
        # message is the same as the tag name
        subprocess.run(
            [
                "git",
                "tag",
                "-f",
                "-a",
                "-m",
                f"Update {spec.name} to {latest}",
                f"{spec.name}-{latest}",
            ]
        )
        # The github webhooks won't fire if 3+ tags are made at once, to be
        # defensive push each tag by itself
        subprocess.run(["git", "push", "--follow-tags"])


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Update versions in RPM Spec files and prepare commits."
    )
    parser.add_argument(
        "-p",
        "--push",
        help="when updating spec files, immediately push updates with "
             "cooresponding tags for COPR",
        action="store_true",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        help="log all information to stdout while running",
        action="store_true",
    )
    parser.add_argument(
        "-d",
        "--dry-run",
        help="do not write new spec files, only print if updates are needed",
        action="store_true",
    )
    parser.add_argument(
        "-i",
        "--in-place",
        help="when updating a spec file, do not store a backup",
        action="store_true",
    )
    parser.add_argument(
        "directory",
        nargs="?",
        help="directory where spec files are located. defaults to the working "
             "directory",
        default=".",
    )
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.INFO)

    update_summary = [
        f"{'Name':15}\t{'Old Version':8}\tNew Version"]

    if (
        args.push
        and subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"], capture_output=True
        ).returncode
        != 0
    ):
        # We're not in a git repository, exit
        logging.error("Cannot use --push when not running in a git repository")
        exit(1)

    for spec_loc in Path(args.directory).glob("**/*.spec"):
        logging.info(f"Starting {spec_loc}")

        spec = parse_spec(spec_loc)
        logging.info(f"Parsed from spec file: {spec}")
        if spec.url.netloc != "github.com":
            logging.warning(
                f"{spec.name} is hosted on {spec.url.netloc} "
                "but this script only checks projects from github, "
                "skipping this file")
            continue

        is_latest, latest = is_latest_version(spec)
        logging.info(f"newest version: {latest}")
        logging.info(f"spec file is latest: {is_latest}")

        ver_string = (
            f"{spec.version:8}\t(no update)" if is_latest
            else f"{spec.version:8}\t{latest:8}"
        )
        update_summary.append(f"{spec.name:15}\t{ver_string}")

        if not is_latest and not args.dry_run:
            logging.info(f"Updating {spec.name}")
            update_version(spec, latest, inplace=args.in_place, push=args.push)

    print("\n".join(update_summary))


if __name__ == "__main__":
    main()
