import json
import os
from pprint import pprint
import time
import traceback
# from urllib.request import urlopen, Request, ProxyHandler, build_opener
import requests

from .air_post import AirPost
from .TelePusher import TelePusher


PHANTOM_URL = os.environ.get("PHANTOM_URL")
PHANTOM_KEY = os.environ.get("PHANTOM_KEY")
BASE_URL = os.environ.get("NG_BASE_URL")
TELEGRAM_CHANNEL = os.environ.get("NG_TELEGRAM_CHANNEL")

class NgException(Exception):
    pass

class Post(object):
    def __init__(self, info, grp):
        self.info = info
        self.grp = grp        

    def get_media_url(self):
        if self.info.get("type") == "Photo":
            return self.info.get("images").get("image700").get("url")
        elif self.info.get("type") == "Animated":
            return self.info.get("images").get("image460sv").get("url")    

    def __str__(self):
        return self.info.get("id")

    def json(self):
        return {
            "id": self.info.get("id"),
            "title": self.info.get("title"),
            "type": self.info.get("type"),
            "url": self.info.get("url"),
            "media_url": self.get_media_url(),
            "group": self.grp
        }

class Ng(object):
    def __init__(self, grp: str, typ: str = "hot"):
        self.grp = grp
        self.typ = typ
    
    def send_latest_posts(self):        
        pusher = TelePusher(chat_id=TELEGRAM_CHANNEL)
        try:
            d = {
                "url": BASE_URL.format(grp=self.grp, typ=self.typ),
                "renderType":"plainText",
                "outputAsJson": "true"
            }

            url = PHANTOM_URL.format(key=PHANTOM_KEY)            
            res = requests.post(url, data=json.dumps(d))            
            
            if res.status_code in [200]:            
                data = res.json()
                
                posts = {}
                
                for post in data.get("data").get("posts"):                    
                    posts[post.get("id")] = Post(post, self.grp).json()
                
                ap = AirPost("appqzdWspiYMEZxLy", "posts")
                inserted_posts = ap.insert(posts, "id")
                
                no_of_posts = len(inserted_posts) 

                pusher.send_message(f"Got {no_of_posts} posts of {self.grp}:{self.typ}")
                time.sleep(5)

                for idx, post in enumerate(inserted_posts):
                    counter = f"{idx + 1}/{no_of_posts}"
                    caption = "{ctr}\nTitle: {title}\n\nURL: {url}".format(ctr=counter, title=post["title"], url=post["url"])
                    if post["type"] == "Photo":
                        pusher.send_photo(photo_url=post["media_url"], caption=caption)
                    elif post["type"] == "Animated":
                        pusher.send_video(video_url=post["media_url"], caption=caption)
                    time.sleep(5)                                
            else:
                raise NgException(f"Invalid status code: {res.status}")
        except Exception as e:            
            msg = f"An error occured while retriving the posts: {e}"
            print(traceback.format_exc())            
            pusher.send_message(text=msg)