import logging
import re
import subprocess

from autocopr.regexconstants import RegexConstants
from autocopr.specdata import SpecData
from githubapi.latest import Latest


def update_version(
    spec: SpecData, latest: Latest, inplace: bool = False, push: bool = False
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

    if inplace:
        spec_loc_backup.unlink()
    else:
        logging.info("Original spec file is at {spec_loc_backup}")

    # Add a commit with this update and tag it so COPR sees it
    if push:
        logging.info("Pushing changes...")
        commit_msg = f"Update {spec.name} to {latest.ver}\n\n{latest.url}"
        subprocess.run(["git", "add", str(spec.loc)])
        subprocess.run(["git", "commit", "-m", commit_msg])
        # Have to make an annotated tag for github to recognize it
        # message is the same as the commit message
        subprocess.run(
            ["git", "tag", "-a", "-m", commit_msg, f"{spec.name}-{latest.ver}"]
        )
        # The github webhooks won't fire if 3+ tags are made at once, to be
        # defensive push each tag by itself
        subprocess.run(["git", "push", "--follow-tags"])
