import logging
from pathlib import Path
from typing import Optional

import requests

from .githubapi import graphql, rest
from .githubapi.latest import Latest
from .specdata import SpecData


def get_latest_versions(specs: list[SpecData], token: Optional[str],
                        id_cache: Path) -> list[tuple[SpecData, Latest]]:
    """Given a list of specs, optionally a Github token, and a location to load
    and store a cache of GraphQL ids, return a list of SpecData with latest version.
    Removes any SpecData that does not have a cooresponding version."""

    if token:
        logging.info(
            "GITHUB_TOKEN environment variable or --github-token flag is set, "
            "using GraphQL api")
        return graphql.latest_versions(specs, token, id_cache)
    else:
        logging.warning(
            "GITHUB_TOKEN environment variable or --github-token flag is not set, "
            "using REST api instead of GraphQL.")
        logging.warning(
            "The REST API requires more connections, gathers more data than is "
            "needed, and you are limited to 60 requests per hour without a token.")

        with requests.Session() as s:
            return [(spec, latest) for spec in specs
                    if (latest := rest.get_latest_version(spec, s)) is not None
                    ]
