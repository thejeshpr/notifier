import os
from pprint import pprint 
import sys
import json
import traceback

import requests
from bs4 import BeautifulSoup

from .TelePusher import TelePusher

BASE_URL = os.environ.get("B_BASE_URL")
DOWNLOAD_END_POINT=os.environ.get("B_DOWNLOAD_END_POINT")


class Bfy(object):
    """
    class for bfy
    """
    def __init__(self):
        """
        Initiliaze
        """
        self.box_id = os.environ.get("BOX_ID")    
        self.no_of_posts = int(os.environ.get("BFY_NO_OF_POSTS")) or 10        
        self.downloaded_posts = []
        channel = os.environ.get('BFY_TELEGRAM_CHANNEL')
        self.pusher = TelePusher(chat_id=channel)
    
    def __get_latest_posts(self):
        """
        get posts posts
        return: posts
        """
        res = requests.get(BASE_URL)
        if res.status_code == 200:
            soup        = BeautifulSoup(res.content, 'html.parser')
            all_cards   = soup.find('div', {'id':'project-grid'})
            posts = all_cards.find_all('div', {'class':['card']})[:self.no_of_posts]
                        
            for post in posts:
                pid = post.find('div', {'class':'simplefavorite-button has-count'}).get('data-postid').strip()
                self.downloaded_posts.append({
                    "id": int(pid),
                    "Name": post.find("h4", {"class":"card-title"}).text.strip(),
                    "URL": post.find('a').get('href')
                })  

    @staticmethod
    def get_download_link(pid):
        return f"{BASE_URL}{DOWNLOAD_END_POINT}{pid}"

    def __format_post(self, post):
        return (f"Name: {post['Name']}\n"
               f"ID: {post['id']}\n"
               f"URL: {post['URL']}\n"
               f"File: {Bfy.get_download_link(post['id'])}\n")

    
    def send(self):
        """
        send latest posts
        """ 
        try:
            self.__get_latest_posts()

            if self.downloaded_posts:
                msg = []
                msg.append(f"Latest bfy posts\n")

                for post in self.downloaded_posts:
                    msg.append(self.__format_post(post))
                                
                msg = "\n".join(msg)
            else:
                msg = "No new posts found"
            error = False
        except Exception as e:
            error = True
            tb = traceback.format_exc()
            msg = "{}\n{}".format(e, tb)
        
        finally:
            status = "Success" if not error else "Error"
            msg = f"Bfy update: {status}\n\n{msg}"            
            self.pusher.send_message(msg, disable_web_page_preview="True")
