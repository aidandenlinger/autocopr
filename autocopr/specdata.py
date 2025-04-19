import logging
import re
import urllib.parse
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from autocopr.regexconstants import RegexConstants
from githubapi.latest import OwnerName


@dataclass(frozen=True)
class SpecData:
    """Data from a parsed spec file."""

    ownerName: OwnerName
    version: str
    loc: Path

    @property
    def name(self) -> str:
        return self.ownerName.name


def parse_spec(spec_loc: Path) -> Optional[SpecData]:
    """Given a path to a Spec file, returns a parsed version and url. Returns
    None if file does not have a name, version, or URL, or if the URL is not a
    Github repo."""

    name = None
    version = None
    url = None

    with open(spec_loc) as spec:
        for line in spec:
            # Assumes Version and URL are only defined once in the file!
            # If there are duplicate definitions, behavior is undefined!
            if (name_match := re.search(RegexConstants.name_pat, line)) is not None:
                logging.info(f'Got name from: "{line.rstrip()}"')
                name = name_match.group(1)
            elif (ver_match := re.search(RegexConstants.version_pat, line)) is not None:
                logging.info(f'Got version from: "{line.rstrip()}"')
                version = ver_match.group(1)
            elif (url_match := re.search(RegexConstants.url_pat, line)) is not None:
                logging.info(f'Got url from: "{line.rstrip()}"')
                # Remove any trailing slashes, we don't them for future API calls
                url = urllib.parse.urlparse(url_match.group(1).rstrip("/"))
                if url.netloc != "github.com":
                    logging.warning(
                        f"{spec_loc} is hosted on {url.netloc} "
                        "but this script only checks projects from github, "
                        "skipping this file"
                    )
                    return None

            if name is not None and version is not None and url is not None:
                ownerName = OwnerName(*url.path[1:].split("/"))
                parsed = SpecData(ownerName, version, spec_loc)
                logging.info(f"Parsed from file: {parsed}")
                return parsed

    logging.warning(f"Missing name, version or URL field in {spec_loc}!")
    return None
