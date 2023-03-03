from requests import post
import os


class Gql():
    def __init__(self):
        self.sid = os.getenv('connect.sid')

    def replit(self, body):
        try:
            return post("https://replit.com/graphql",
                        json=body,
                        headers={
                            "Referer": "https://replit.com",
                            "X-Requested-With": "replit",
                            "Cookie": "connect.sid=" + self.sid
                        }).json()
        except:
            return {
                "id": -1,
                "title": "undefined",
                "descriptionPreview": "undefined",
                "cycles": -1,
                "deadline": "0000-00-06T00:00:00.000Z",
                "slug": "undefined",
                "timeCreated": "0000-00-06T00:00:00.000Z",
                "applicationCount": -1,
                "user": {
                    "url": "/@undefined"
                },
                "__typename": "Bounty",
                "url": "https://replit.com/bounties/@undefined/undefined",
                "timestamp": "<t:0000000000:R>",
                "dollars": "$-1.00"
            }
