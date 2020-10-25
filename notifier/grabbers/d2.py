import urllib.parse
from notifier.grabbers.base import Base, Internet


class D2(object):    

    @staticmethod
    def sync(obj: Base, *args, **kwargs):    
        soup = Internet.get_soup(obj.sync_type.base_url)
        divs = soup.find_all('div', {'class':'crayons-story__indention'})

        for div in divs[::-1]:
            a = div.find('a')
            url = urllib.parse.urljoin(obj.sync_type.base_url, a.get('href'))
            obj.add_text_task(
                unique_key=a.get('id').strip(),
                name=a.text.strip(),
                url=url,
                data=dict(text=url)
            )
