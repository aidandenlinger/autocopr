from dataclasses import dataclass


@dataclass(frozen=True)
class Latest:
    ver: str
    url: str
