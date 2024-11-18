import logging
from typing import Optional

import requests
from githubapi.latest import Latest, OwnerName, clean_tag


def get_latest_version(spec: OwnerName, session: requests.Session) -> Optional[Latest]:
    """Given SpecData with a github url, returns the latest version. Forces
    usage of a session because all uses of this function will use the same
    API. Returns None if there is no latest version (either the repo has no
    releases, or you are rate limited by Github. Unauthenticated users only get
    60 requests per hour -
    https://docs.github.com/en/rest/overview/resources-in-the-rest-api?apiVersion=2022-11-28#rate-limits-for-requests-from-personal-accounts
    )"""

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
        logging.warning(f"{spec.name} does not have a latest version, skipping")
        logging.info("Request received:")
        import json

        logging.info(json.dumps(req, indent=4))
        return None

    # Trims tags like "v0.35.2" to "0.35.2" by cutting from the front until we
    # hit a digit
    # If your project's tags aren't as simple, this will need to be edited
    # RPM versions don't start with letters
    # Assumes the version has a digit somewhere in it
    latest_version = clean_tag(latest_tag)
    logging.info(f"{spec.name} latest version is {latest_version}")

    return Latest(latest_version, latest_url)
