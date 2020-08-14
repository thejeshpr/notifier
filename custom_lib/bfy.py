import os
from pprint import pprint 
import sys
import json
import traceback

import requests
from bs4 import BeautifulSoup
from airtable import Airtable

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
        self.collection = "b-posts"
        self.existing_posts_id = []
        self.new_posts = []
        self.new_posts_id = []
        self.downloaded_posts = {}   
        self.error = None
        self.pusher = TelePusher()
        self.airtable = Airtable('appLC2o0lmr4Pc6rU', 'posts')        
    
    def __get_post_ids(self):
        """
        get posts posts
        return: posts
        """
        res = requests.get(BASE_URL)
        if res.status_code == 200:
            soup        = BeautifulSoup(res.content, 'html.parser')
            all_cards   = soup.find('div', {'id':'project-grid'})
            posts = all_cards.find_all('div', {'class':['card']})            
                        
            for post in posts:
                pid = post.find('div', {'class':'simplefavorite-button has-count'}).get('data-postid').strip()                
                self.downloaded_posts[pid] = {
                    "id": int(pid),
                    "Name": post.find("h4", {"class":"card-title"}).text.strip(),                    
                    "URL": post.find('a').get('href')
                }

    def __get_all_existing_posts(self):
        """
        get data from jbox
        return: posts
        """
        records = self.airtable.get_all(fields=['id'])
        for record in records:
            self.existing_posts_id.append(record['fields'].get('id'))
        self.existing_posts_id.sort()        
            
    
    def __compare_posts(self):
        """
        compare existing posts and new posts
        return: new posts
        """
        # Get downloaded post ids and sort it
        downloaded_posts_id = [int(x) for x in list(self.downloaded_posts.keys())]
        downloaded_posts_id.sort()        

        if not self.existing_posts_id == downloaded_posts_id:
            self.new_posts = list(set(downloaded_posts_id) - set(self.existing_posts_id))

    @staticmethod
    def get_download_link(pid):
        return f"{BASE_URL}{DOWNLOAD_END_POINT}{pid}"

    def __format_post(self, post):
        return (f"Name: {post['Name']}\n"
               f"ID: {post['id']}\n"
               f"URL: {post['URL']}\n"
               f"File: {Bfy.get_download_link(post['id'])}\n")

    
    def sync(self):
        """
        Sync the posts
        """ 
        try:
            self.__get_post_ids()
            self.__get_all_existing_posts()            
            self.__compare_posts()            

            if self.new_posts:                
                msg = []
                msg.append(f"{len(self.new_posts)} post(s) found")
                posts_to_push = []

                for post_id in self.new_posts:                    
                    data = self.downloaded_posts[str(post_id)]
                    posts_to_push.append(data)
                    msg.append(self.__format_post(data))
                
                self.airtable.batch_insert(posts_to_push)
                msg = "\n".join(msg)                
            else:
                msg = "No new posts found"                      
            tb = ""
            error = False

        except Exception as e:
            error = True
            tb = traceback.format_exc()
            msg = "{}\n{}".format(e, tb)
        
        finally:
            status = "Success" if not error else "Error"
            msg = f"Bfy update: {status}\n\n{msg}"            
            self.pusher.send_message(msg)
