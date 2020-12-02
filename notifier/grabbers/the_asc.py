import urllib.parse
from notifier.grabbers.base import Base, Internet


class TheAsc(object):    

    @staticmethod
    def sync(obj: Base, *args, **kwargs):
                
        r = Internet.html_get(obj.sync_type.base_url)

        found_links = []

        xpaths = obj.sync_type.extras.get("xp")        

        for xpath in xpaths:
            links = r.html.xpath(xpath)            
            if links:
                found_links.extend(links)                

        for a in found_links[::-1]:                   
            url = a.attrs.get('href').split("?")[0]            
            name = a.text.strip().replace("\n", " - ")

            obj.add_text_task(
                unique_key=url,
                name=name,
                url=url,
                data={}
            )
