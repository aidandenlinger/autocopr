import argparse
import asyncio
import httpx
import logging
import subprocess
import re
import urllib.parse
from typing import Optional
from pathlib import Path
from dataclasses import dataclass


# From https://github.com/bkircher/python-rpm-spec, thanks!
name_pat = re.compile(r"^Name\s*:\s*(\S+)", re.IGNORECASE)
version_pat = re.compile(r"^Version\s*:\s*(\S+)", re.IGNORECASE)
url_pat = re.compile(r"^URL\s*:\s*(\S+)", re.IGNORECASE)
release_pat = re.compile(r"^Release\s*:\s*(\S+)", re.IGNORECASE)


@dataclass(frozen=True)
class SpecData:
    """Data from a parsed spec file."""
    name: str
    version: str
    url: urllib.parse.ParseResult
    loc: Path


def parse_spec(spec_loc: Path) -> Optional[SpecData]:
    """Given a path to a Spec file, returns a parsed version and url. Returns
    None if file does not have a name, version, or URL, or if the URL is not a
    Github repo."""

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
                if url.netloc != "github.com":
                    logging.warning(
                        f"{spec_loc} is hosted on {url.netloc} "
                        "but this script only checks projects from github, "
                        "skipping this file")
                    return None

            if name is not None and version is not None and url is not None:
                parsed = SpecData(name, version, url, spec_loc)
                logging.info(f"Parsed from file: {parsed}")
                return parsed

    logging.warning(f"Missing name, version or URL in {spec_loc}! Skipping")
    return None


async def get_latest_versions(
        specs: list[SpecData]) -> list[tuple[SpecData, str]]:
    """Async runner to get the latest versions for all Specs.
    Disregards specs that do not have a latest version."""
    # Use a client since we're querying the same API multiple times
    async with httpx.AsyncClient() as c:
        return [(spec, latest) for spec in specs
                if (latest := await get_latest_version(spec, c)) is not None]


async def get_latest_version(
    spec: SpecData, client: httpx.AsyncClient
) -> Optional[str]:
    """Given SpecData with a github url, returns the latest version. Forces
    usage of a session because all uses of this function will use the same
    API. Returns None if there is no latest version (either the repo has no
    releases, or you are rate limited by Github. Unauthenticated users only get
    60 requests per hour -
    https://docs.github.com/en/rest/overview/resources-in-the-rest-api?apiVersion=2022-11-28#rate-limits-for-requests-from-personal-accounts
    )"""

    project_info = spec.url.path[1:]
    url = f"https://api.github.com/repos/{project_info}/releases/latest"
    logging.info(f"Querying {url}")

    raw_req = await client.get(
        url,
        params={"X-GitHub-Api-Version": "2022-11-28",
                "Accept": "application/vnd.github+json"},
    )
    req = raw_req.json()

    try:
        latest_tag: str = req["tag_name"]
    except KeyError:
        logging.warning(
            f"{spec.name} does not have a latest version, skipping")
        logging.info("Request received:")
        import json
        logging.info(json.dumps(req, indent=4))
        return None

    # Trims tags like "v0.35.2" to "0.35.2" by cutting from the front until we
    # hit a digit
    # If your project's tags aren't as simple, this will need to be edited
    # RPM versions don't start with letters
    # Assumes the version has a digit somewhere in it
    first_digit = [x.isdigit() for x in latest_tag].index(True)
    latest_version = latest_tag[first_digit:]
    logging.info(f"{spec.name} latest version is {latest_version}")

    return latest_version


def update_version(
    spec: SpecData, latest: str, inplace: bool = False, push: bool = False
):
    """Given the location of a spec file, the latest version, and the name of
    the package, update the version in the spec and make a commit with the
    cooresponding COPR tag."""

    logging.info(f"Updating {spec.name} file to {latest}...")
    spec_loc_backup = spec.loc.rename(
        spec.loc.with_suffix(spec.loc.suffix + ".bak"))

    with (open(spec.loc, "w") as new_spec, open(spec_loc_backup) as old_spec):
        # Again, assumes that Version and Release are only defined once!
        for line in old_spec:
            if re.match(version_pat, line):
                new_spec.write(f"Version: {latest}\n")
            elif re.match(release_pat, line):
                # All new versions must start at release 1
                new_spec.write("Release: 1%{?dist}\n")
            else:
                new_spec.write(line)

    if inplace:
        spec_loc_backup.unlink()
    else:
        logging.info("Original spec file is at {spec_loc_backup}")

    # Add a commit with this update and tag it so COPR sees it
    if push:
        logging.info("Pushing changes...")
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


def create_parser() -> argparse.ArgumentParser:
    """Initializes the cli parser."""

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

    return parser


def main():
    args = create_parser().parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.INFO)

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

    specs: list[SpecData] = [parsed for spec
                             in Path(args.directory).glob("**/*.spec")
                             if (parsed := parse_spec(spec)) is not None]

    latest_ver = asyncio.run(get_latest_versions(specs))

    update_summary = [
        f"{'Name':15}\t{'Old Version':8}\tNew Version"]

    update_summary += [f"{spec.name:15}\t{spec.version:8}\t"
                       f"{'(no update)' if spec.version == latest else latest}"
                       for (spec, latest) in latest_ver]

    if not args.dry_run:
        for (spec, latest) in latest_ver:
            if spec.version != latest:
                update_version(
                    spec, latest, inplace=args.in_place, push=args.push)

    print("\n".join(update_summary))

    if args.dry_run:
        print("To update the spec files, run again without the dry-run flag.")
    elif not args.in_place:
        print("If any specs were updated, the original spec files now have a "
              ".bk suffix, and the spec files are updated with the newest "
              "version.")
    else:
        print("Any updates have been applied to the spec files.")


if __name__ == "__main__":
    main()
