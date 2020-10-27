import urllib.parse
from notifier.grabbers.base import Base, Internet


class BKdko(object):    

    @staticmethod
    def sync(obj: Base, *args, **kwargs):        
        soup = Internet.get_soup_phjs(obj.sync_type.base_url)
        divs = soup.find_all('div', {'class':'card card_news shadowWPadding'})[:15]

        for div in divs[::-1]:                
            content_div = div.find('div', {'class': 'gsc_col-sm-7 gsc_col-lg-8 holder'})            
            a = content_div.find('h2').find('a')

            link = a.get('href')                        
            p = content_div.find('p', {'class':'hidden-xs'})
            
            url = urllib.parse.urljoin(obj.sync_type.extras.get('post_url'), link)
            name = a.text.strip()    
            desc = p.text.strip() if p else ""        

            obj.add_text_task(
                unique_key=url,
                name=name,
                url=url,
                data=dict(text=url, desc=desc)
            )

    @staticmethod
    def bkdko_road_test(obj: Base, *args, **kwargs):        
        soup = Internet.get_soup_phjs(obj.sync_type.base_url)
        divs = soup.find_all('div', {'class':'card card_news shadowWPadding'})[:15]

        for div in divs[::-1]:                
            content_div = div.find('div', {'class': 'gsc_col-sm-7 gsc_col-lg-8 holder'})            
            a = content_div.find('h2').find('a')

            link = a.get('href')                        
            p = content_div.find('p', {'class':'hidden-xs'})
            
            url = urllib.parse.urljoin(obj.sync_type.extras.get('post_url'), link)
            name = a.text.strip()    
            desc = p.text.strip() if p else ""  

            print(url, name, desc)      

            obj.add_text_task(
                unique_key=url,
                name=name,
                url=url,
                data=dict(text=url, desc=desc)
            )