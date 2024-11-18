import argparse
import os


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
        "--github-token",
        default=os.environ.get("GITHUB_TOKEN"),
        help=(
            "Github token to use to access the GraphQL API. "
            "Defaults to GITHUB_TOKEN environment variable if not set."
        ),
    )
    parser.add_argument(
        "directory",
        nargs="?",
        help="directory where spec files are located. defaults to the working "
        "directory",
        default=".",
    )

    return parser
