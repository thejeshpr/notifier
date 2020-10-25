import urllib.parse
from notifier.grabbers.base import Base, Internet


class RP(object):    

    @staticmethod
    def sync(obj: Base, *args, **kwargs):    
        soup = Internet.get_soup_phjs(obj.sync_type.base_url)
        banner_div = soup.find('div', {'class':'card-body m-0 p-0 pt-3'})

        a = banner_div.find('a')
        link = urllib.parse.urljoin(obj.sync_type.base_url, a.get('href').strip())
        name = a.text.strip()
        obj.add_text_task(
            unique_key=link,
            name=name,
            url=link,
            data=dict(title=name, text=link)
        )

        # find remaining div
        divs = soup.find_all('div', {'class': "card-body m-0 p-0 mt-2"})[::-1]

        for div in divs:
            a = div.find('a')
            link = urllib.parse.urljoin(obj.sync_type.base_url, a.get('href').strip())
            name = a.text.strip()
            obj.add_text_task(
                unique_key=link,
                name=name,
                url=link,
                data=dict(
                    title=name,
                    text=link
                )
            )




