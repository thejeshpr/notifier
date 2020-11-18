from urllib.parse import urlparse, urljoin
from notifier.grabbers.base import Base, Internet


class BPanda(object):    

    @staticmethod
    def sync(obj: Base, *args, **kwargs):            
        cat = kwargs.get("cat", "")
        typ = kwargs.get("typ", "")
        url = obj.sync_type.base_url.format(cat=cat, typ=typ)        
                          
        res = Internet.html_get(url)
        links = res.html.xpath("/html/body/main/section/article[*]/h2/a")
                
        for a in links[::-1]:            
            link = a.attrs.get("href").split("?")[0]            
            name = a.text.strip()
                        
            obj.add_text_task(
                unique_key=link,
                name=name,
                url=link,
                data={}
            )
