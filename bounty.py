import os
from pathlib import Path
import json
from datetime import datetime

from dotenv import load_dotenv

load_dotenv()

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

BOUNTIES_CACHE_LENGTH = 1

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


def check_for_updates():
    bounties = driver.execute_async_script(BOUNTY_FETCH)

    # Add some custom properties to each bounty that will be handy later
    for bounty in bounties:
        bounty['url'] = "https://replit.com/bounties" + bounty['user'][
            'url'] + '/' + bounty['slug']
        utc_time = datetime.strptime(bounty['deadline'],
                                     "%Y-%m-%dT%H:%M:%S.%fZ")
        epoch_time = (utc_time - datetime(1970, 1, 1)).total_seconds()
        bounty['timestamp'] = f'<t:{int(epoch_time)}:R>'
        bounty['dollars'] = "${:.2f}".format(bounty['cycles'] / 100)

    old_bounty = json.loads(Path('bounties.json').read_text('utf-8'))
    if old_bounty is None:
        old_bounty = {'id': -1}

    # We're up-to-date
    if bounties[0]['id'] <= old_bounty[0]['id']:
        return None
    else:
        # Get the previous N bounties from the new bounties
        new_bounty = bounties[0]

        Path('bounties.json').write_text(json.dumps(new_bounty), 'utf-8')
        return new_bounty
