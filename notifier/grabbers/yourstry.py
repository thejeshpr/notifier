import urllib.parse
from notifier.grabbers.base import Base, Internet


class YS(object):    

    @staticmethod
    def sync(obj: Base, *args, **kwargs):        
        category = kwargs.get("category", "Startup")
        url = obj.sync_type.base_url.format(category=category)        
        soup = Internet.get_soup_phjs(url)
        
        lis = soup.find_all('li', {'class':'sc-hMFtBS gpleaq'})[::-1]      
        # li are returend in double

        for li in lis:            
            a       = li.find('a')            
            div     = li.find('div', {'class':'sc-gqPbQI iIXuvz'})            
            title_a = div.find("a")

            name = title_a.text.strip()

            if name.strip() == "":
                continue
            
            link = urllib.parse.urljoin(obj.sync_type.base_url, a.get('href').strip())
            obj.add_text_task(
                unique_key=link,
                name=name,
                url=link,
                data=dict(text=link)
            )