import urllib.parse
from notifier.grabbers.base import Base, Internet


class Avidhya(object):    

    @staticmethod
    def sync(obj: Base, *args, **kwargs):
                
        r = Internet.html_get(obj.sync_type.base_url)
        links = r.html.xpath('/html/body/div[1]/div[2]/div/div[4]/div[2]/section/div[*]/div[*]/div[2]/a')                                      
                              
        for a in links[::-1]:
            url = a.attrs.get('href').split("?")[0]            
            name = a.text.strip()            

            obj.add_text_task(
                unique_key=url,
                name=name,
                url=url,
                data=dict(text=url)
            )
