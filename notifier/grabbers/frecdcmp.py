import urllib.parse
from notifier.grabbers.base import Base, Internet


class FreCdCmp(object):    

    @staticmethod
    def sync(obj: Base, *args, **kwargs):

        base_url = obj.sync_type.base_url
        res = Internet.html_get(base_url)
        h2_list = res.html.find(".post-card-title")[::-1]

        for h2 in h2_list:
            a = h2.find("a", first=True)
            link = urllib.parse.urljoin(base_url, a.attrs.get('href'))
            print(a.text.strip(), link)
            obj.add_text_task(
                unique_key=link,
                name=a.text.strip(),
                url=link,
                data={}
            )
