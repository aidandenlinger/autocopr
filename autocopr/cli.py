import argparse
import os
from enum import StrEnum


class Mode(StrEnum):
    """
    How the script will operate (ie is it read-only, will it push new files to github, etc)
    """

    Check = "check"
    """
    Manual updates. The job succeeds if all specfiles are up to date and fails
    if any are outdated. This mode does not write new files or push any updates -
    updating the specfile requires manual action. This mode is more secure since the
    action is read-only.
    """

    Push = "push"
    """
    Automated updates. Can only be run in a git repo. If any specfile are
    outdated, write new specfiles, make a commit for each with an associated
    tag, and push it to the repo. Requires `contents: write` permissions on the
    GITHUB_TOKEN to allow for pushes to a repo. See the `README.md` to learn how
    to start a COPR build based on these commits being pushed.

    If using the GraphQL API, generates "graphql_id_cache.json" in the root directory.
    This file should persist across runs. It's recommended to cache it for CI or
    check it into your repo.
    """

    DryRun = "dry-run"
    """
    Intended for testing. The job is read-only and always succeeds, no matter if
    the specfiles are up to date or not. Like all other modes, it logs to stdout
    which files are up to date or not.
    """

    Update = "update"
    """
    Intended to run outside of a git repo. If a spec file is outdated, it
    writes a new specfile at the original path, leaving the original specfile at
    "original_name.spec.bak".
    """


def create_parser() -> argparse.ArgumentParser:
    """Initializes the cli parser."""

    parser = argparse.ArgumentParser(
        description="Check or update RPM spec files to the project's latest version released on Github"
    )
    parser.add_argument(
        "-m",
        "--mode",
        help=""" The desired behavior for this script. `check` is the default option - it is read only, it exits successfully if all spec files are up to date and otherwise exits with an error. `push` will fully automate updates by making and pushing git commits. See the README.md for more info on all available options.""",
        type=Mode,
        choices=list(Mode),
        default=Mode.Check,
    )
    parser.add_argument(
        "-v",
        "--verbose",
        help="Log all information to stdout while running",
        action="store_true",
    )
    parser.add_argument(
        "--github-token",
        default=os.environ.get("GITHUB_TOKEN"),
        help=(
            "Github token to use to access the GraphQL API. "
            "Defaults to GITHUB_TOKEN environment variable if not set."
        ),
    )
    parser.add_argument(
        "--rest",
        help="Forces usage of the Github REST API over the GraphQL API. The GraphQL API is preferred since it typically only needs to make one request.",
        action="store_true",
    )
    parser.add_argument(
        "directory",
        nargs="?",
        help="Directory where spec files are located. defaults to the working "
        "directory",
        default=".",
    )

    return parser
