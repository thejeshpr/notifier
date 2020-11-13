from urllib.parse import urlparse, urljoin
from notifier.grabbers.base import Base, Internet


class FML(object):    

    @staticmethod
    def sync(obj: Base, *args, **kwargs):            
        cat = kwargs.get("cat", "")        
        url = obj.sync_type.base_url.format(cat=cat)        
        
        res = Internet.html_get(url)

        xpaths = [
            "/html/body/main/div[2]/div/div/div[1]/div/div[2]/div/article[*]/div/div[2]/a",
            "/html/body/main/div[2]/div/div/div[1]/div/article[*]/div/div[2]/a",
        ]

        links = []

        for xpath in xpaths:
            links = res.html.xpath(xpath)
            if links: break
        
        f_url = obj.sync_type.extras.get("base_url")
        
        for a in links[::-1]:            
            link = urljoin(f_url, a.attrs.get("href"))
            name = a.text.strip().replace("\n", "--")
            
            obj.add_text_task(
                unique_key=link,
                name=name,
                url=link,
                data={}
            )
