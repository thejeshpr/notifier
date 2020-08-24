import json
import os
from pprint import pprint
import time
import traceback
from urllib.request import urlopen, Request


from .air_post import AirPost
from .TelePusher import TelePusher


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
            url = BASE_URL.format(grp=self.grp, typ=self.typ)                        
            headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}
            
            req = Request(url=url, headers=headers) 
            res = urlopen(req)            
            
            if res.status in [200]:            
                data = json.loads(res.read())

                posts = {}
                
                for post in data.get("data").get("posts"):                    
                    posts[post.get("id")] = Post(post, self.grp).json()
                
                ap = AirPost("appqzdWspiYMEZxLy", "posts")
                inserted_posts = ap.insert(posts, "id")
                
                pusher.send_message(f"Sending {len(inserted_posts)} posts of {self.grp}:{self.typ}")
                time.sleep(5)

                for post in inserted_posts:
                    caption = "Title: {title}\n\nURL: {url}".format(title=post["title"], url=post["url"])
                    if post["type"] == "Photo":                        
                        pusher.send_photo(photo_url=post["media_url"], caption=caption)
                    elif post["type"] == "Animated":
                        pusher.send_video(video_url=post["media_url"], caption=caption)
                    time.sleep(5)                                
            else:
                raise NgException(f"Invalid status code: {res.status}")            
        except Exception as e:            
            msg = f"An error occured while retriving the posts: {e}\n{traceback.format_exc()}"
            pusher.send_message(text=msg)                    
