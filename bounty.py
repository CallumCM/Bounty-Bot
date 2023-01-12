import requests
from bs4 import BeautifulSoup
from pathlib import Path
import json

BOUNTY_URL = "https://replit.com/bounties"

BOUNTIES_CACHE_LENGTH = 10

HEADERS = {
    'User-agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582'
}


def fetch_bounties(soup):
    bounties_list = soup.find("ul",
                              class_="css-ph3dp7").find_all("li",
                                                            recursive=False)

    bounties = []

    for bounty_element in bounties_list:
        dollars = bounty_element.select(
            'div > div > div.css-1p35i8v > div > span.css-1vcini8'
        )[0].get_text(strip=True)
        cycles = bounty_element.select(
            'div > div > div.css-1p35i8v > div > span.css-1dfa7l9 > div.css-uoocf6 > span'
        )[0].get_text(strip=True)

        url = 'https://replit.com' + bounty_element.select(
            'div > a')[0]['href']

        description = bounty_element.select('div > div > span')[0].get_text(
            strip=True)

        title = bounty_element.select('div > div > h3')[0].get_text(strip=True)

        due_in = ' '.join(
            bounty_element.select(
                'div > div > div.css-1p35i8v > span > div.css-1pwjctj > span')
            [0].get_text(strip=True).split(' ')[2:])

        #author = bounty_element.select(
        #    'div > div > div.css-11g7lfh > div:nth-child(1) > a > span > span > div > div.css-12zqyc0 > span'
        #)[0].get_text(strip=True)

        bounties.append({
            "dollars": dollars,
            "cycles": cycles,
            "url": url,
            "description": description,
            "title": title,
            "due_in": due_in,
            #"author": author
        })

    return bounties[::-1]


def check_for_updates():
    bounty_page = requests.get(BOUNTY_URL, headers=HEADERS)
    bounty_page.encoding = bounty_page.apparent_encoding

    soup = BeautifulSoup(bounty_page.text, features="html.parser")

    old_bounty_page = Path('prev_bounty.html').read_text('utf-8')
    old_bounties = json.loads(Path('bounties.json').read_text('utf-8'))

    bounties_updated = old_bounty_page != bounty_page

    if bounties_updated:
        new_bounties = fetch_bounties(soup)
        new_bounty_index = len(new_bounties) - 1

        # Figure out how many bounties behind we are, since this doesn't update in realtime
        for i, bounty in enumerate(new_bounties):
            if len(old_bounties) == 0 or bounty == old_bounties[-1]:
                new_bounty_index = i + 1

        Path('prev_bounty.html').write_text(
            json.dumps(new_bounties[new_bounty_index:]), 'utf-8')
        return new_bounties[new_bounty_index:]
    else:
        return None
