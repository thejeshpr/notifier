import urllib.parse
from notifier.grabbers.base import Base, Internet


class Crdko(object):    

    @staticmethod
    def sync(obj: Base, *args, **kwargs):

        res = Internet.html_get(obj.sync_type.base_url)
        links = res.html.xpath("/html/body/div[2]/div/div[1]/div/main/div[3]/div[1]/div[1]/div/div[*]/div[2]/h2/a")

        for a in links[::-1]:            

            link = a.attrs.get('href')            
            url = urllib.parse.urljoin(obj.sync_type.extras.get('post_url'), link)
            name = a.text.strip()                        
            
            obj.add_text_task(
                unique_key=url,
                name=name,
                url=url,
                data=dict(text=url)
            )

    
    @staticmethod
    def crdko_road_test(obj: Base, *args, **kwargs):        

        res = Internet.html_get(obj.sync_type.base_url)
        links = res.html.xpath("/html/body/div[2]/div/div[1]/div/main/div[3]/div[1]/div/div[1]/div/div[*]/div[2]/h2/a")
        

        for a in links[::-1]:
            
            link = a.attrs.get('href')            
            url = urllib.parse.urljoin(obj.sync_type.extras.get('post_url'), link)
            name = a.text.strip()            
            
            obj.add_text_task(
                unique_key=url,
                name=name,
                url=url,
                data=dict(text=url)
            )