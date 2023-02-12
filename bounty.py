import os
from pathlib import Path
import json
from datetime import datetime

import nextcord
from dotenv import load_dotenv
from gql import Gql

load_dotenv()

BOUNTIES_CACHE_LENGTH = 5

BOUNTY_QUERY = """
query BountiesPageSearch($input: BountySearchInput!) {
  bountySearch(input: $input) {
    __typename
    ... on BountySearchConnection {
      items {
        ...BountyCard
        __typename
      }
      pageInfo {
        hasNextPage
        nextCursor
        __typename
      }
      __typename
    }
    ... on UserError {
      message
      __typename
    }
    ... on UnauthorizedError {
      message
      __typename
    }
  }
}

fragment BountyCard on Bounty {
  id
  title
  descriptionPreview
  cycles
  deadline
  slug
  timeCreated
  applicationCount
  user {
    url
  }
}
"""

GRAPHQL_PAYLOAD = [{
    "operationName": "BountiesPageSearch",
    "variables": {
        "input": {
            "count": BOUNTIES_CACHE_LENGTH,
            "searchQuery": "",
            "status": "open",
            "order": "creationDateDescending"
        }
    },
    "query": BOUNTY_QUERY
}]

gql = Gql(os.getenv('connect.sid'))


def calculate_new_bounties(old_bounties, new_bounties):

    # If we don't end up finding a match between old and new bounties,
    # there's more new bounties than BOUNTIES_CACHE_LENGTH.

    # While this is highly unlikely, in the future
    # I'd like to add support for this so that it'll
    # fetch more bounties until it finds a match,
    # to ensure none are missed.

    legitimately_new_bounties = []

    for i, bounty in enumerate(new_bounties):
        if not bounty['id'] in [
                old_bounty['id'] for old_bounty in old_bounties
        ]:
            print('New Bounty: ' + bounty['title'])
            legitimately_new_bounties.append(bounty)
        else:
            print('Old Bounty: ' + bounty['title'])

    print('-' * 25)

    return legitimately_new_bounties


def create_bounties_json_if_needed():
    """If bounties.json does not exist, create it"""
    if not os.path.isfile('bounties.json'):
        Path('bounties.json').write_text('[]', 'utf-8')


def most_recent_bounty():
    """Fetch the most recent bounty cached in bounties.json"""
    create_bounties_json_if_needed()
    old_bounties = json.loads(Path('bounties.json').read_text('utf-8'))
    if len(old_bounties) > 0:
        return old_bounties[-1]
    else:
        return None


def create_bounty_embed(bounty):
    embed = nextcord.Embed(title=bounty['title'],
                           url=bounty["url"],
                           description=bounty["descriptionPreview"],
                           color=0xe75f0a)

    embed.add_field(name="Pays",
                    value=f'{bounty["dollars"]} ({bounty["cycles"]} Cycles)')

    embed.add_field(name='Deadline', value=bounty['timestamp'])

    return embed


def check_for_updates():
    print("Fetching new bounties...")

    # Bounties we fetched from Replit
    fetched_bounties = gql.replit(
        GRAPHQL_PAYLOAD)[0]['data']['bountySearch']['items'][::-1]

    print("Fetched new bounties")

    for new_bounty in fetched_bounties:

        # Add some custom properties to the bounty that will be handy later
        new_bounty['url'] = "https://replit.com/bounties" + new_bounty['user'][
            'url'] + '/' + new_bounty['slug']
        utc_time = datetime.strptime(new_bounty['deadline'],
                                     "%Y-%m-%dT%H:%M:%S.%fZ")
        epoch_time = (utc_time - datetime(1970, 1, 1)).total_seconds()
        new_bounty['timestamp'] = f'<t:{int(epoch_time)}:R>'
        new_bounty['dollars'] = "${:.2f}".format(new_bounty['cycles'] / 100)

    # Bounties that exist in bounties.json
    create_bounties_json_if_needed()
    old_bounties = json.loads(Path('bounties.json').read_text('utf-8'))
    if len(old_bounties) == 0:
        old_bounties = [{'id': -1}]

    new_bounties = calculate_new_bounties(old_bounties, fetched_bounties)

    if new_bounties:
        Path('bounties.json').write_text(json.dumps(fetched_bounties), 'utf-8')
        return new_bounties
    else:
        return None
