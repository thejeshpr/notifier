import urllib.parse
from notifier.grabbers.base import Base, Internet


class Autocrind(object):    

    @staticmethod
    def sync(obj: Base, *args, **kwargs):        

        res = Internet.html_get(obj.sync_type.base_url)
        links = res.html.xpath("/html/body/form/div[4]/div[3]/div/div[1]/div[*]/div/div[1]/h3/a")

        for a in links[::-1]:                
            
            link = a.attrs.get('href')                                                
            url = urllib.parse.urljoin(obj.sync_type.base_url, link)

            name = a.text.strip()

            obj.add_text_task(
                unique_key=url,
                name=name,
                url=url,
                data=dict(text=url)
            )
