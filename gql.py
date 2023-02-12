from requests import post


class Gql():
    def __init__(self, sid):
        self.sid = sid

    def replit(self, body):
        return post("https://replit.com/graphql",
                    json=body,
                    headers={
                        "Referer": "https://replit.com",
                        "X-Requested-With": "replit",
                        "Cookie": "connect.sid=" + self.sid
                    }).json()
