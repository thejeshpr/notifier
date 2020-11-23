import urllib.parse
from notifier.grabbers.base import Base, Internet


class GSM(object):    

    @staticmethod
    def sync(obj: Base, *args, **kwargs):
                
        r = Internet.html_get(obj.sync_type.base_url)

        links = []
        
        xpaths = obj.sync_type.extras.get("xp")        

        for xpath in xpaths:
            links = r.html.xpath(xpath)            
            if links: break    
        
        article_url = obj.sync_type.extras.get("article_url")

        for a in links[::-1]:            
            path = a.attrs.get('href')
            url = urllib.parse.urljoin(article_url, path)
            name = a.text.strip()

            obj.add_text_task(
                unique_key=url,
                name=name,
                url=url,
                data={}
            )
