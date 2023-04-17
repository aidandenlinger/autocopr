import logging
from typing import Optional

import requests

from .githubapi import graphql, rest
from .githubapi.latest import Latest
from .specdata import SpecData


def get_latest_versions(specs: list[SpecData],
                        token: Optional[str]) -> list[tuple[SpecData, Latest]]:
    """Given a list of specs, return a list of SpecData with latest version.
    Removes any SpecData that does not have a cooresponding version."""
    if token:
        logging.info(
            "GITHUB_TOKEN environment variable or --github-token flag is set, "
            "using GraphQL api")
        return graphql.latest_versions(specs, token)
    else:
        logging.warning(
            "GITHUB_TOKEN environment variable or --github-token flag is not set, "
            "using REST api")

        with requests.Session() as s:
            return [(spec, latest) for spec in specs
                    if (latest := rest.get_latest_version(spec, s)) is not None
                    ]
