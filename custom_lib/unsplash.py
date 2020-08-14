import os
import traceback

import requests

from .TelePusher import TelePusher

class Unsplash():
    def __init__(self):
        self.__url = "https://api.unsplash.com/photos/"
        self.__access_token = os.environ.get("UNSPLASH_ACCESS_TOKEN")
    
    def send_random_image(self):
        url = self.__url + "random"
        pusher = TelePusher()
        try:
            params = {
                "client_id": self.__access_token                
            }
            res = requests.get(url, params=params).json()
            img = res.get('links').get('download')
            user = res.get('user').get('name')
            pusher.send_photo(
                img, caption=f'User: {user}'
                )            
        except Exception as e:            
            tb = traceback.format_exc()
            msg = f"Unsplash: Error\n\n{e}\n{tb}"
            pusher.send_message(msg)
        