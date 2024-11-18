from dataclasses import dataclass


@dataclass(frozen=True)
class Latest:
    """Information about the latest Github Release."""

    ver: str
    url: str


def clean_tag(tag: str) -> str:
    """Given a tag, trim it until its first digit to get an rpm version."""
    # Trims tags like "v0.35.2" to "0.35.2" by cutting from the front until we
    # hit a digit
    # If your project's tags aren't as simple, this will need to be edited
    # RPM versions don't start with letters
    # Assumes the version has a digit somewhere in it
    first_digit = [x.isdigit() for x in tag].index(True)
    version = tag[first_digit:]
    return version


@dataclass(frozen=True)
class OwnerName:
    owner: str
    name: str

    def id(self) -> str:
        """Return the string "owner/name" """
        return self.owner + "/" + self.name
