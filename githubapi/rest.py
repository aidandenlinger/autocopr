import logging
from typing import Optional

import requests
from githubapi.latest import Latest, OwnerName, clean_tag


def get_latest_version(spec: OwnerName, session: requests.Session) -> Optional[Latest]:
    """
    Retrieves the latest release version of a GitHub repository using the GitHub API.

    Args:
        spec: An object representing the GitHub repository identifier.

    Returns:
        A Latest object containing the cleaned version string and release URL, or None if the repository has no releases or the API response is missing expected fields.
    """

    url = f"https://api.github.com/repos/{spec.id()}/releases/latest"
    logging.info(f"Querying {url}")

    req = session.get(
        url,
        params={
            "X-GitHub-Api-Version": "2022-11-28",
            "Accept": "application/vnd.github+json",
        },
    ).json()

    try:
        latest_tag: str = req["tag_name"]
        latest_url: str = req["html_url"]
    except KeyError:
        logging.warning(f"{spec.name} does not have a latest version!")
        logging.warning("Request received:")
        import json

        logging.warning(json.dumps(req, indent=4))
        return None

    # Trims tags like "v0.35.2" to "0.35.2" by cutting from the front until we
    # hit a digit
    # If your project's tags aren't as simple, this will need to be edited
    # RPM versions don't start with letters
    # Assumes the version has a digit somewhere in it
    latest_version = clean_tag(latest_tag)
    logging.info(f"{spec.name} latest version is {latest_version}")

    return Latest(latest_version, latest_url)
