import os

import requests
from bs4 import BeautifulSoup
from jsonbox import JsonBox

from custom_lib import response_handler, push



BASE_URL        = os.environ.get("B_BASE_URL")
DOWNLOAD_URL    = f"{BASE_URL}/test-file/?wpdmdl="
NAME            = "buildofy-posts"
NOTIFICATION_TYPE = "Buildofy Status"

pusher = push.Push(os.environ.get("WIREPUSHER_ID"))
jb = JsonBox()

class Buildofy(object):
    """
    class for buildofy
    """
    @staticmethod
    def __get_post_ids():
        """
        get posts posts
        return: posts
        """
        res = requests.get(BASE_URL)
        if res.status_code == 200:
            soup        = BeautifulSoup(res.content, 'html.parser')
            all_cards   = soup.find('div', {'id':'project-grid'})
            pids        = all_cards.find_all('div', {'class':'simplefavorite-button has-count'})
            
            return [post.get('data-postid').strip() for post in pids]
       
    @staticmethod
    def __get_posts_frm_jsnbx(box_id):
        """
        get data from jbox
        return: posts
        """
        res = jb.read(box_id, query=f"name:{NAME}")
        return res[0]

    @staticmethod
    def __compare_posts(jbox_res, current_posts):
        """
        compare existing posts and new posts
        return: new posts
        """
        existing_posts = jbox_res.get('ids')        
        existing_posts.sort()
        current_posts.sort()

        if not existing_posts == current_posts:
            return list(set(current_posts) - set(existing_posts))
            

    @staticmethod
    def __push_to_jbox(posts, box_id, id=None):
        """
        Push data to jbox        
        """
        payload = {
            "name": NAME,
            "ids": posts
        }

        if id:
            jb.update(payload, box_id, id)
        else:
            jb.write(payload, box_id)

    @staticmethod
    def sync(box_id):
        """
        Sync the posts
        """ 
        try:            
            posts = Buildofy.__get_post_ids()            

            if posts:
                jbox_res = Buildofy.__get_posts_frm_jsnbx(box_id)
                
                if jbox_res:
                    new_posts = Buildofy.__compare_posts(jbox_res, posts)

                    if new_posts:

                        updated_posts = jbox_res.get("ids") + new_posts                        

                        Buildofy.__push_to_jbox(updated_posts, box_id, jbox_res.get('_id'))
                        pusher.push(
                            title=f"Buildofy Status",
                            message=f"{len(new_posts)} post(s) found: {','.join(new_posts)}",
                            notification_type=NOTIFICATION_TYPE
                        )

                    else:
                        pusher.push(
                            title=f"Buildofy Status",
                            message=f"No new posts found",
                            notification_type=NOTIFICATION_TYPE
                        )

                else:
                    Buildofy.__push_to_jbox(posts)    
            else:
                pusher.push(
                    title=f"Buildofy Status: error",
                    message=f"coundn't get posts from site",
                    notification_type=NOTIFICATION_TYPE
                )

        except Exception as e:
            pusher.push(
                title=f"Buildofy Status: Error",
                message=f"An error occurred while retreiving posts: {e}",
                notification_type=NOTIFICATION_TYPE
            )            

    @staticmethod
    def get_download_link(post_id):
        """
        returns the download link of given post
        return: download link
        """
        return f'{DOWNLOAD_URL}{post_id}'    
        