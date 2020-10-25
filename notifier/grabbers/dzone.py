import urllib.parse
from notifier.grabbers.base import Internet, Base


class Dzone(object):    

    @staticmethod
    def sync(obj: Base, *args, **kwargs):        
        url = obj.sync_type.base_url                
        article_url = obj.sync_type.extras.get('article_url')

        res = Internet.post_phjs(url, return_json=True)                
        posts = res['result']['data']['nodes'][::-1]

        for post in posts:
            post['text'] = urllib.parse.urljoin(article_url, post.get('articleLink'))
            obj.add_text_task(
                unique_key=post.get('id'),                
                name=post['title'],
                url=post['text'],
                data=post
            )
