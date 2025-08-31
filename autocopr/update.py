import logging
import os
import re
import subprocess

from autocopr.regexconstants import RegexConstants
from autocopr.specdata import SpecData
from githubapi.latest import Latest


def update_version(
    spec: SpecData, latest: Latest, push: bool = False, verbose: bool = False
):
    """Given the location of a spec file, the latest version, and the name of
    the package, update the version in the spec and make a commit with the
    cooresponding COPR tag."""

    logging.info(f"Updating {spec.name} file to {latest.ver}...")
    spec_loc_backup = spec.loc.rename(spec.loc.with_suffix(spec.loc.suffix + ".bak"))

    with open(spec.loc, "w") as new_spec, open(spec_loc_backup) as old_spec:
        # Again, assumes that Version and Release are only defined once!
        for line in old_spec:
            if re.match(RegexConstants.version_pat, line):
                new_spec.write(f"Version: {latest.ver}\n")
            elif re.match(RegexConstants.release_pat, line):
                # All new versions must start at release 1
                new_spec.write("Release: 1%{?dist}\n")
            else:
                new_spec.write(line)

    if not push:
        logging.info(f"Original spec file is at {spec_loc_backup}")
        return

    # Otherwise, we're pushing changes!

    spec_loc_backup.unlink()  # Remove backup
    logging.info("Pushing changes...")

    add_result = subprocess.run(
        ["git", "add", str(spec.loc.absolute().relative_to(os.getcwd()))],
        capture_output=(not verbose),
    )
    if add_result.returncode:
        if not verbose:
            logging.error(add_result.stderr)

        logging.error(
            f"Failed to add {spec.loc} to the working repository.\nThis is a bug, please report it. Exiting..."
        )
        exit(1)

    commit_msg = f"Update {spec.name} to {latest.ver}\n\n{latest.url}"
    commit_result = subprocess.run(["git", "commit", "-m", commit_msg], capture_output=(not verbose))
    if commit_result.returncode:
        logging.error(
            "Failed to make a commit.\nThis is a bug, please report it. Exiting..."
        )
        exit(1)

    # Have to make an annotated tag for github to recognize it
    # message is the same as the commit message
    tag_result = subprocess.run(
        ["git", "tag", "-a", "-m", commit_msg, f"{spec.name}-{latest.ver}"],
        capture_output=(not verbose),
    )
    if tag_result.returncode:
        if not verbose:
            logging.error(add_result.stderr)

        logging.error(
            "Failed to make a tag.\nThis is a bug, please report it. Exiting..."
        )
        exit(1)

    # The github webhooks won't fire if 3+ tags are made at once, to be
    # defensive we push on each spec file rather than pushing at the end
    push_result = subprocess.run(["git", "push", "--follow-tags"], capture_output=(not verbose))
    if push_result.returncode:
        if not verbose:
            logging.error(add_result.stderr)

        logging.error(
            "Failed to push updates to the github repo.\nIf you're using Github Actions, please ensure your job has `contents: write` permissions to be able to push to the repo.\nExiting..."
        )
        exit(1)
