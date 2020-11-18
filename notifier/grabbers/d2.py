import urllib.parse
from notifier.grabbers.base import Base, Internet


class D2(object):    

    @staticmethod
    def sync(obj: Base, *args, **kwargs):        
        
        cat = kwargs.get("cat", "")
        url = urllib.parse.urljoin(obj.sync_type.base_url, cat)        
        res = Internet.html_get(url)
        h2_list = res.html.find(".crayons-story__title")        

        for h2 in h2_list[::-1]:            
            a = h2.find('a', first=True)

            url = urllib.parse.urljoin(obj.sync_type.base_url, a.attrs.get('href'))

            obj.add_text_task(
                unique_key=a.attrs.get('id').strip(),
                name=a.text.strip(),
                url=url,
                data=dict(text=url)
            )
