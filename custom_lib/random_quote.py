import os

import requests

from custom_lib import push

NOTIFICATION_TYPE = "Random Quote"

pusher = push.Push(os.environ.get("WIREPUSHER_ID"))

class RandomQuote(object):
    URL = "https://thesimpsonsquoteapi.glitch.me/quotes"
    def __init__(self):
        """
        Initialize
        """
        pass 

    def get_quote(self):
        try:
            res = requests.get(RandomQuote.URL)
            if res.status_code == 200:
                data = res.json()
                pusher.push(
                    title="Random Quote",
                    message=data[0].get("quote"),
                    notification_type=NOTIFICATION_TYPE                    
                )
            else:
                pusher.push(
                    title="Random Quote: error",
                    message=f"An error occurred while fetching random quote, status code: {res.status_code}",
                    notification_type=NOTIFICATION_TYPE
                )
        except Exception as e:
            pusher.push(
                    title="Random Quote: error",
                    message=f"An error occurred while fetching random quote: {e}",
                    notification_type=NOTIFICATION_TYPE
                )