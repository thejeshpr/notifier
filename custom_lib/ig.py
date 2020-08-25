import os
import requests
import json
import time
from pprint import pprint

from air_post import AirPost
from TelePusher import TelePusher

TELEGRAM_CHANNEL = os.environ.get("IG_TELEGRAM_CHANNEL")

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
        username = self.profile['graphql']['user']['username']
        igid = self.profile['graphql']['user']['id']
        edges = self.profile.get("graphql")\
                            .get("user")\
                            .get("edge_owner_to_timeline_media")\
                            .get('edges')

        posts = {}

        for edge in edges:
            node = edge.get('node')
            if node["__typename"] in ["GraphImage", "GraphVideo"]:
                _id = node.get("id")
                posts[_id] = Posts(igid, username, node).json()

        # pprint(posts)

        ap = AirPost("appgFYflbwfpBuhRp", "posts")
        inserted_posts = ap.insert(posts, "igid")

        if inserted_posts:
            pusher.send_message(f"Sending {len(inserted_posts)} posts of {username}")
            time.sleep(5)

            for post in inserted_posts:
                print(post["code"])
                if post['is_video']:
                    print(pusher.send_video(video_url=post["video_url"], caption=post["caption"]))
                else:
                    print(pusher.send_photo(photo_url=post["disp_url"], caption=post["caption"])            )
                    
                time.sleep(5)   
        else:
            pusher.send_message(f"no latest posts of found for user {username}")


if __name__ =="__main__":
    # i = IG("")
    # i.send_latest_posts()