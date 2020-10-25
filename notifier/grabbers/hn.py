import urllib.parse
from notifier.grabbers.base import Base, Internet


class HN(object):    

    @staticmethod
    def sync(obj: Base, *args, **kwargs):
        
        tag = kwargs.get("tag", "programming")
        url = obj.sync_type.base_url.format(tag=tag)
        post_url = obj.sync_type.extras.get("post_url")        
        soup = Internet.get_soup_phjs(url)        
        posts = soup.find_all('div', {'class':'title-wrapper'})[::-1]

        for post in posts:
            a = post.find('a')            
            link = urllib.parse.urljoin(post_url, a.get('href').strip())            
            obj.add_text_task(
                unique_key=link,
                name=a.text.strip(),
                url=link,
                data=dict(
                    title=a.text.strip(),
                    text=link
                )
            )




