import os
from notifier.grabbers.base import Base, Internet


class Ng(object):    

    @staticmethod
    def sync(obj: Base, *args, **kwargs):

        group, typ = (
                kwargs.get("group") or os.environ.get("NG_DEFAULT_GROUP"),
                kwargs.get("type") or os.environ.get("NG_DEFAULT_TYPE")
            )


        url = obj.sync_type.base_url.format(grp=group, typ=typ)
        data = Internet.post_phjs(url=url, return_json=True)

        posts = data.get("data").get("posts")[::-1]

        for post in posts:
            
            data = {                
                "caption": "{}\n{}".format(post.get("title"), post.get("url")),
                "title": post.get("title"),
                "nsfw": post.get("nsfw"),
                "post_url": post.get("url"),
                "content_type": post.get("type"),
                "up_vote": post.get("upVoteCount"),
                "down_vote": post.get("downVoteCount"),
                "description": post.get("description"),
                "comments_count": post.get("commentsCount"),                
            }

            # check post type
            if post["type"] == "Photo":
                data["url"] = post.get("images").get("image700").get("url")
                obj.add_photo_task(
                    unique_key=post.get("id"),
                    name=post['title'],
                    url=data["url"],
                    data=data
                )  

            elif post["type"] == "Animated":
                data["url"] = post.get("images").get("image460sv").get("url")
                obj.add_video_task(
                    unique_key=post.get("id"),
                    name=post['title'],
                    url=data["url"],
                    data=data
                )
