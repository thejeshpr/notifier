import urllib.parse
from notifier.grabbers.base import Base, Internet


class Crdko(object):    

    @staticmethod
    def sync(obj: Base, *args, **kwargs):        
        soup = Internet.get_soup_phjs(obj.sync_type.base_url)
        divs = soup.find_all('div', {'class':'card card_news shadowWPadding'})                

        for div in divs[::-1]:
            content_div = div.find_all('div')[2]
            a = content_div.find('h2').find('a')

            link = a.get('href')            
            url = urllib.parse.urljoin(obj.sync_type.extras.get('post_url'), link)
            name = a.text.strip()
            p = content_div.find('p', {'class':'hidden-xs'})
            
            desc = p.text.strip() if p else ""
            
            obj.add_text_task(
                unique_key=url,
                name=name,
                url=url,
                data=dict(text=url, desc=desc)
            )

    
    @staticmethod
    def crdko_road_test(obj: Base, *args, **kwargs):
        soup = Internet.get_soup_phjs(obj.sync_type.base_url)
        divs = soup.find_all('div', {'class':'card card_news shadowWPadding'})                

        for div in divs[::-1]:
            content_div = div.find_all('div')[2]
            a = content_div.find('h2').find('a')

            link = a.get('href')            
            url = urllib.parse.urljoin(obj.sync_type.extras.get('post_url'), link)
            name = a.text.strip()
            p = content_div.find('p', {'class':'hidden-xs'})
            
            desc = p.text.strip() if p else ""
            
            obj.add_text_task(
                unique_key=url,
                name=name,
                url=url,
                data=dict(text=url, desc=desc)
            )
            
