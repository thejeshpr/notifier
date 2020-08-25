import os
import requests
import json
import time
from pprint import pprint

from .air_post import AirPost
from .TelePusher import TelePusher

TELEGRAM_CHANNEL = os.environ.get("IG_TELEGRAM_CHANNEL")
IG_POST_URL = os.environ.get("IG_POST_CODE")

class Posts(object):
    def __init__(self, igid, username, node):
        self.igid = igid
        self.username = username
        self.code = node.get("shortcode")
        self.disp_url = node.get("display_url")
        self.is_video = node.get("is_video")
        self.video_url = node.get("video_url")

        if node.get('edge_media_to_caption'):
            self.caption = node.get('edge_media_to_caption').get('edges')[0]\
                            .get('node').get('text')
        else:
            self.caption = ""

        
    def __str__(self):
        return self.code

    def json(self):
        return {
            "igid": self.igid,
            "username": self.username,
            "code": self.code,
            "disp_url": self.disp_url,
            "caption": self.caption,
            "is_video": self.is_video,
            "video_url": self.video_url
        }


class IG(object):
    def __init__(self, un):        
        self.url = os.environ.get("IG_BASE_URL")
        self.un = un
        self.profile = self.get_profile()        

    def get_profile(self):
        headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}
        return requests.get(self.url.format(self.un), headers=headers).json()

    def send_latest_posts(self):
        pusher = TelePusher(chat_id=TELEGRAM_CHANNEL)
        try:            
            username = self.profile['graphql']['user']['username']
            igid = self.profile['graphql']['user']['id']
            edges = self.profile.get("graphql")\
                                .get("user")\
                                .get("edge_owner_to_timeline_media")\
                                .get('edges')

            posts = {}

            for edge in edges:
                node = edge.get('node')                
                code = node.get("shortcode")
                posts[code] = Posts(igid, username, node).json()            

            ap = AirPost("appgFYflbwfpBuhRp", "posts")
            inserted_posts = ap.insert(posts, "code")

            if inserted_posts:
                pusher.send_message(f"Sending {len(inserted_posts)} posts of {username}")
                time.sleep(5)

                for post in inserted_posts:
                    code = post["code"]                    
                    pusher.send_message(text=IG_POST_URL.format(code=code))
                    time.sleep(5)   
            else:
                pusher.send_message(f"no latest posts of found for user {username}")
        except Exception as e:
            pusher.send_message(f"An error occured while fetcing posts of user: {self.un}")