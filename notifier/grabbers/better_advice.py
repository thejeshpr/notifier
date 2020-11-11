import urllib.parse
from notifier.grabbers.base import Base, Internet


class BetterAdvice(object):    

    @staticmethod
    def sync(obj: Base, *args, **kwargs):
                
        r = Internet.html_get(obj.sync_type.base_url)
        links = r.html.xpath('/html/body/div[*]/div[*]/div/div[*]/div[*]/section/div[*]/div[*]/div[*]/a')        

        for a in links[::-1]:            
            url = urllib.parse.urljoin(obj.sync_type.base_url, a.attrs.get('href'))
            name = a.text.strip()            

            obj.add_text_task(
                unique_key=url,
                name=name,
                url=url,
                data=dict(text=url)
            )
