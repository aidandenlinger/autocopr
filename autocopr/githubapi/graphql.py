import json
import logging
from pathlib import Path

import requests

from ..specdata import SpecData
from .latest import Latest, clean_tag

# The GraphQL API allows us to specify exactly what we want, instead of
# overfetching data we don't need from the REST API. This means that
# we can have one connection to query all our repos at once, instead of
# one connection per repo, and save network traffic from data we don't
# need.
#
# However, it also introduces new requirements to deal with:
# - We have to provide a Github token to use it. Doesn't cost money, but
#   definitely more setup than REST.
# - Idiomatic GraphQL does not use string interpolation to make queries
#   ("we should never be doing string interpolation to construct queries from
#   user-supplied values." - https://graphql.org/learn/queries/#variables)
#   However, the Github GraphQL API doesn't allow us to submit a list of
#   repositories, it only allows us to submit a list of node IDs. This means
#   we need to maintain a repository -> node mapping locally, but once we have
#   this cache we can refer to it for all future queries. So it's O(n)
#   connections to get the repository IDs, but O(1) connections after we have
#   this mapping.
#
# So overall approach:
# - Get our spec -> ID mapping
# - If we have new specs without an ID, get their IDs and update the cache
# - Once we have all IDs, query repository information for them
# - Map the GraphQL response to a Latest object (or disregard nulls) and return it

graphQL_url = "https://api.github.com/graphql"
ID = str


def update_cache(id_cache: Path, specs: list[SpecData], headers: dict[str,
                                                                      str],
                 session: requests.Session) -> list[tuple[SpecData, ID]]:
    """Given a list of specs, request headers, id cache, and session,
    load the cache of id keys and fetch any new ones from GraphQl"""

    if id_cache.exists():
        with open(id_cache) as cache:
            ids = json.load(cache)

        logging.info(f"Loaded IDs for {ids.keys()} from {id_cache}")
    else:
        ids = {}
        logging.info(f"No cache at {id_cache}, making a new one")

    specs_that_need_key = [
        spec for spec in specs if spec.ownerName() not in ids
    ]

    # GraphQL query that takes an owner and name, returns its id
    get_id_query = """
    query GetID($owner: String!, $name: String!) {
      repository(owner: $owner, name: $name) {
        id
      }
    }    
    """

    specs_that_got_added = []
    for spec in specs_that_need_key:
        owner, name = spec.ownerName().split("/")
        logging.info(f"Getting key for {spec.name} ({owner=}, {name=})")

        resp = session.post(graphQL_url,
                            json={
                                "query": get_id_query,
                                "variables": {
                                    "owner": owner,
                                    "name": name
                                }
                            },
                            headers=headers).json()

        if "errors" in resp:
            logging.warning(
                f"API error when getting {spec.name}'s GraphQL id':")
            for error in resp['errors']:
                logging.warning(error['message'])
            logging.warning(f"Skipping {spec.name}...")

            continue

        try:
            id = resp['data']['repository']['id']
        except KeyError:
            logging.warning(f"Error accessing id for {spec.name}, skipping")
            logging.warning("API response:")
            logging.warning(resp)
            continue

        logging.info(f"Adding {id=} for {spec.name} to cache")
        specs_that_got_added.append(spec.name)
        ids[spec.ownerName()] = id

    if len(specs_that_got_added) > 0:
        # We changed the cache, update it
        logging.info(
            f"Writing new GraphQL cache since {specs_that_got_added} added")
        with open(id_cache, "w") as out:
            json.dump(ids, out, indent=2)
    else:
        logging.info("No new GraphQL keys added")

    # Finally, map ids to their actual specs and return!
    return [(spec, ids[ownername]) for spec in specs
            if (ownername := spec.ownerName()) in ids]


def get_latest_versions(
        spec_ids: list[tuple[SpecData, ID]], headers: dict[str, str],
        session: requests.Session) -> list[tuple[SpecData, Latest]]:

    # Special case this because the response won't have any data and will
    # throw a key error. On all other instances we will have data.
    if len(spec_ids) == 0:
        return []

    # Query an id, if it's a repository (in our case it is) get the latest
    # release name and url
    latest_versions = """
        query GetLatest($ids: [ID!]!) {
          nodes(ids: $ids) {
            ... on Repository {
              latestRelease {
                tagName
                url
              }
            }
          }
        }
    """

    resp = session.post(graphQL_url,
                        json={
                            "query": latest_versions,
                            "variables": {
                                "ids": [id for (_, id) in spec_ids]
                            }
                        },
                        headers=headers).json()

    spec_releases = []
    for (spec, node) in zip((spec for (spec, _) in spec_ids),
                            resp['data']['nodes']):
        if node and (latest := node['latestRelease']) and 'tagName' in latest:
            latest_version = clean_tag(latest['tagName'])
            logging.info(f"{spec.name} latest version is {latest_version}")
            spec_releases.append((spec, Latest(latest_version, latest['url'])))
        else:
            logging.warning(
                f"Error getting latest release from {spec.name}. Skipping")
            logging.info(f"Node response: {node}")

    if "errors" in resp:
        logging.warning("GraphQL errors when checking latest versions:")
        for error in resp['errors']:
            logging.warning(error['message'])

    return spec_releases


def latest_versions(specs: list[SpecData], token: str,
                    id_cache: Path) -> list[tuple[SpecData, Latest]]:
    """Given a list of specs, a github token, and a location to load and store
    a cache of GraphQL ids, get the latest versions for all the specs given."""

    with requests.session() as session:
        headers = {
            "Authorization": f"bearer {token}",
            # https://docs.github.com/en/graphql/guides/migrating-graphql-global-node-ids
            # Even though it's 2023, still need to hand in this header to get
            # the latest IDs :shrug:
            "X-Github-Next-Global-ID": "1"
        }

        spec_ids = update_cache(id_cache, specs, headers, session)

        return get_latest_versions(spec_ids, headers, session)
