import urllib.parse
from notifier.grabbers.base import Base, Internet


class Crwle(object):    

    @staticmethod
    def sync(obj: Base, *args, **kwargs):            
        soup = Internet.get_soup_phjs(obj.sync_type.base_url)
        links = soup.find_all('a', {'class':'o-eZTujG o-fyWCgU'})

        for a in links[::-1]:                                        

            link = a.get('href')                                    
            
            url = urllib.parse.urljoin(obj.sync_type.base_url, link)            
            name = a.text.strip()            

            obj.add_text_task(
                unique_key=url,
                name=name,
                url=url,
                data=dict(text=url)
            )
