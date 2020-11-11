from urllib.parse import urlparse, urljoin
from notifier.grabbers.base import Base, Internet


class FML(object):    

    @staticmethod
    def sync(obj: Base, *args, **kwargs):            
        cat = kwargs.get("cat", "")        
        url = obj.sync_type.base_url.format(cat=cat)
        print(url)
                
        soup = Internet.get_soup_phjs(url)        
        links = soup.find_all('a', {'class':'article-link'})        
        f_url = obj.sync_type.extras.get("base_url")

        for a in links[::-1]:                        
            link = urljoin(f_url, a.get("href"))            
            name = a.text.strip().replace("\n", "--")
            
            obj.add_text_task(
                unique_key=link,
                name=name,
                url=link,
                data={}
            )
