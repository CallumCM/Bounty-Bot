import os
from pathlib import Path
import json
from datetime import datetime

from dotenv import load_dotenv

load_dotenv()

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

BOUNTIES_CACHE_LENGTH = 5

BOUNTY_URL = "https://replit.com/bounties"
GRAPHQL_URL = "https://replit.com/graphql"

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

COOKIES = {'connect.sid': os.getenv('connect.sid')}

HEADERS = {
    'User-agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    "Content-Type": "application/json",
    "X-Requested-With": "XMLHttpRequest"
}

BOUNTY_FETCH = f"""const callback = arguments[arguments.length - 1]; 
fetch(\"{GRAPHQL_URL}", {{
  "headers": {{
    "Accept": "*/*",
    "Content-Type": "application/json",
    "X-Requested-With": "XMLHttpRequest",
    "Cookie": {json.dumps(COOKIES)}
  }},
  "body": JSON.stringify({json.dumps(GRAPHQL_PAYLOAD)}),
  "method": "POST",
}}).then(response => {{
  response.json().then(data => {{
    callback(data[0].data.bountySearch.items.reverse());
  }});
}});
"""


def init():
    global driver
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(BOUNTY_URL)


def calculate_new_bounties(old_bounties, new_bounties):

    # If we don't end up finding a match between old and new bounties,
    # there's more new bounties than BOUNTIES_CACHE_LENGTH.

    # While this is highly unlikely, in the future
    # I'd like to add support for this so that it'll
    # fetch more bounties until it finds a match,
    # to ensure none are missed.

    new_bounties_end_index = 0
    for i, bounty in enumerate(new_bounties):
        if not bounty in old_bounties:
            print(bounty['title'])
            new_bounties_end_index = i + 1

    return new_bounties[:new_bounties_end_index]


def check_for_updates():

    # Bounties we fetched from Replit
    fetched_bounties = driver.execute_async_script(BOUNTY_FETCH)

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
    old_bounties = json.loads(Path('bounties.json').read_text('utf-8'))
    if len(old_bounties) == 0:
        old_bounties = [{'id': -1}]

    new_bounties = calculate_new_bounties(old_bounties, fetched_bounties)

    if new_bounties:
        Path('bounties.json').write_text(json.dumps(fetched_bounties), 'utf-8')
        return new_bounties
    else:
        return None
