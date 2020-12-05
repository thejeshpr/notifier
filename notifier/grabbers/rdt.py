from requests_html import HTML

import urllib.parse
from notifier.grabbers.base import Base, Internet


class Rdt(object):    

    @staticmethod
    def sync(obj: Base, *args, **kwargs):

        base_url = obj.sync_type.base_url
        cats = obj.sync_type.extras.get("cats")
        ad_identifier = obj.sync_type.extras.get("ad_identifier")
        found_links = {}

        # xpaths = obj.sync_type.extras.get("xp")        
        # post_base_url = obj.sync_type.extras.get("post_base_url")
        # all_links = []        

        cat = kwargs.get("cat")        

        if cat and cat in cats:
            url = urllib.parse.urljoin(base_url, cats.get(cat))
        else:
            url = base_url                
        
        res = Internet.html_get(url)
    
        for p in res.html.find(".top-matter"):
            a = p.find("a", first=True)
            if a:
                link = a.attrs.get("href")
                if link not in found_links and not link.startswith(ad_identifier):
                    li = p.find(".first", first=True)
                    comment = li.find("a", first=True)
                    comment_link = comment.attrs.get('href')
                    comment_link = comment_link.replace("old.reddit.com", "www.reddit.com")
                    found_links[a.text.strip()] = comment_link
                            
        for title, cmt_link in found_links.items():            
            obj.add_text_task(
                    unique_key=cmt_link,
                    name=title,
                    url=cmt_link,
                    data={}
                )
                    