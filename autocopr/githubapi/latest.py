from dataclasses import dataclass


@dataclass(frozen=True)
class Latest:
    """Information about the latest Github Release."""
    ver: str
    url: str
