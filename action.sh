#!/bin/bash
#
# Parses Github Actions args and runs autocopr
#
# Requires these environment variables to be defined:
# - ROOT_LOC: the root directory to start searching for spec files. Must be a path relative to the working directory.
# - MODE: The mode the script is running in - `check`, `push`, or any other acceptable argument to `--mode`. See `action.yml`/`README.md` for more details.
#
# Optional environment variables:
# - GITHUB_TOKEN: An authenticated Github token. Highly recommended to be defined to avoid rate limits! Needs `contents:write` permissions for "push" mode.
# - VERBOSE: if the script should log all information to stdout - should be "true" or "false" (default)

set -Eeuxo pipefail # https://vaneyckt.io/posts/safer_bash_scripts_with_set_euxo_pipefail/

args=()

# mode - let python's parsing reject any invalid input
args+=("--mode" "$MODE")

# verbose - case insensitive comparison, so it'll accept True or true
VERBOSE=${VERBOSE:-false}
if [ "${VERBOSE,,}" = "true" ]; then
  args+=("--verbose")
fi

# The folder where *this* script is, so we can run autocopr.py.
# (Technically unneeded, this should be put in the environment by action.yml, but nice for testing this script locally.)
# https://stackoverflow.com/a/11114547
ACTIONS_FOLDER=$(dirname "$(realpath --no-symlinks "${BASH_SOURCE[0]}")")

python "${ACTIONS_FOLDER}"/main.py "${args[@]}" "${ROOT_LOC}"
