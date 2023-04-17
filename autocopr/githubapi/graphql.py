import logging

from ..specdata import SpecData
from .latest import Latest


def latest_versions(specs: list[SpecData],
                    token: str) -> list[tuple[SpecData, Latest]]:
    logging.error("GraphQL API in progress")
    exit()
