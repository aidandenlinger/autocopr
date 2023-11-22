import logging
from pathlib import Path
from typing import Optional

import requests

import githubapi.graphql
import githubapi.rest
from autocopr.specdata import SpecData
from githubapi.latest import Latest, OwnerName


def get_latest_versions(specs: list[SpecData], token: Optional[str],
                        id_cache: Path) -> list[tuple[SpecData, Latest]]:
    """Given a list of specs, optionally a Github token, and a location to load
    and store a cache of GraphQL ids, return a list of SpecData with latest version.
    Removes any SpecData that does not have a cooresponding version."""

    if token:
        logging.info(
            "GITHUB_TOKEN environment variable or --github-token flag is set, "
            "using GraphQL api")

        ownerNames = [
            OwnerName(*spec.ownerName().split("/")) for spec in specs
        ]

        latest = githubapi.graphql.latest_versions(ownerNames, token, id_cache)

        final = []
        for ownerName, ver in latest:
            # There will be a matching spec because we generated ownerNames from our spec list
            matchingSpec = next(spec for spec in specs
                                if spec.ownerName() == ownerName.id())

            final.append((matchingSpec, ver))

        return final
    else:
        logging.warning(
            "GITHUB_TOKEN environment variable or --github-token flag is not set, "
            "using REST api instead of GraphQL.")
        logging.warning(
            "The REST API requires more connections, gathers more data than is "
            "needed, and you are limited to 60 requests per hour without a token."
        )

        with requests.Session() as s:
            return [
                (spec, latest_ver) for spec in specs
                if (latest_ver := githubapi.rest.get_latest_version(
                    OwnerName(*spec.ownerName().split("/")), s)) is not None
            ]
