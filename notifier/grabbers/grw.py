import os
from notifier.grabbers.base import Base, Internet


class Grw(object):    

    @staticmethod
    def sync(obj: Base, *args, **kwargs):

        # https://groww.in/slr/v1/search/derived/scheme?available_for_investment=true&doc_type=scheme&page=0&plan_type=Direct&q=&size=16&sort_by=3
        # sort_by 1: Rating High to low
        # sort_by 2: Rating Low to high
        # sort_by 3: Rating popularity        
        data = Internet.post_phjs(url=obj.sync_type.base_url, return_json=True)['content']
        
        for post in data.get("data").get("posts"):
            
            data = {                
                "caption": "{}\n{}".format(post.get("title"), post.get("url")),
                "title": post.get("title"),
                "nsfw": post.get("nsfw"),
                "post_url": post.get("url"),
                "content_type": post.get("type"),
                "up_vote": post.get("upVoteCount"),
                "down_vote": post.get("downVoteCount"),
                "description": post.get("description"),
                "comments_count": post.get("commentsCount")
            }

            # check post type
            if post["type"] == "Photo":
                data["url"] = post.get("images").get("image700").get("url")
                obj.add_photo_task(
                    unique_key=post.get("id"),
                    name=post['title'],
                    url=post.get("url"),
                    data=data
                )  

            elif post["type"] == "Animated":
                data["url"] = post.get("images").get("image460sv").get("url")
                obj.add_video_task(
                    unique_key=post.get("id"),
                    name=post['title'],
                    url=post.get("url"),
                    data=data
                )
