import urllib.parse
from notifier.grabbers.base import Base, Internet


class Thephoblographer(object):    

    @staticmethod
    def sync(obj: Base, *args, **kwargs):
                
        r = Internet.html_get(obj.sync_type.base_url)
        links = r.html.find(".entry-title")

        for h2 in links[::-1]:
            a = h2.find("a", first=True)
            url = a.attrs.get('href')            
            name = a.text.strip()            

            obj.add_text_task(
                unique_key=url,
                name=name,
                url=url,
                data={}
            )
