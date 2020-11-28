from requests_html import HTML

import urllib.parse
from notifier.grabbers.base import Base, Internet


class Rdt(object):    

    @staticmethod
    def sync(obj: Base, *args, **kwargs):

        base_url = obj.sync_type.base_url
        xpaths = obj.sync_type.extras.get("xp")
        all_links = []

        cats = {
            "popular": "/r/popular/",
            "popular-india": "r/popular/?geo_filter=IN",
            "popular-everywhere": "/r/popular/?geo_filter=GLOBAL",
            "popular-us": "r/popular/?geo_filter=US",
            "popular-new": "r/popular/new/",
            "popular-today": "r/popular/top",
            "popular-week": "r/popular/top/?t=week",
            "popular-month": "r/popular/top/?t=month",
            "python": "r/Python/",
        }

        cat = kwargs.get("cat")        

        if cat and cat in cats:
            url = urllib.parse.urljoin(base_url, cats.get(cat))
        else:
            url = base_url                

        doc = Internet.post_phjs(url, render_type="html", output_as_json="false")
        html = HTML(html=doc)
        
        for xpath in xpaths:            
            links = html.xpath(xpath)                        
            if links:
                all_links.extend(links)        
        
        for a in all_links[::-1]:            
            path = a.attrs.get('href')
            url = urllib.parse.urljoin(base_url, path)
            name = a.text.strip()

            obj.add_text_task(
                unique_key=url,
                name=name,
                url=url,
                data={}
            )
