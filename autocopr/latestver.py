import requests
from .specdata import SpecData
from .githubapi import rest
from .githubapi.latest import Latest


def get_latest_versions(
    specs: list[SpecData]
) -> list[tuple[SpecData, Latest]]:
    """Given a list of specs, return a list of SpecData with latest version.
    Removes any SpecData that does not have a cooresponding version."""
    with requests.Session() as s:
        return [(spec, latest)
                for spec in specs
                if (latest := rest.get_latest_version(spec, s))
                is not None]
