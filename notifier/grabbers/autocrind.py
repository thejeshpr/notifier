import urllib.parse
from notifier.grabbers.base import Base, Internet


class Autocrind(object):    

    @staticmethod
    def sync(obj: Base, *args, **kwargs):        
        soup = Internet.get_soup_phjs(obj.sync_type.base_url)
        divs = soup.find_all('div', {'class':'blog row'})

        for div in divs[::-1]:                
            content_div = div.find('div', {'class': 'inner'})
            a = content_div.find('h3').find('a')

            link = a.get('href')                                    
            
            url = urllib.parse.urljoin(obj.sync_type.base_url, link)
            name = a.text.strip()
            
            obj.add_text_task(
                unique_key=url,
                name=name,
                url=url,
                data=dict(text=url)
            )
