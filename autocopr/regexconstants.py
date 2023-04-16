import re


class RegexConstants:
    # From https://github.com/bkircher/python-rpm-spec, thanks!
    name_pat = re.compile(r"^Name\s*:\s*(\S+)", re.IGNORECASE)
    version_pat = re.compile(r"^Version\s*:\s*(\S+)", re.IGNORECASE)
    url_pat = re.compile(r"^URL\s*:\s*(\S+)", re.IGNORECASE)
    release_pat = re.compile(r"^Release\s*:\s*(\S+)", re.IGNORECASE)
