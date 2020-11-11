import urllib.parse
from notifier.grabbers.base import Base, Internet


class DeepSt(object):    

    @staticmethod
    def sync(obj: Base, *args, **kwargs):
        
        url = "https://deepstash.com/trending"
        soup = Internet.get_soup_phjs(url)        
        links = soup.find_all('a', {'class':'css-rgh4li'})[::-1]

        print(len(links))
        links = links[::-1][:-1]
        print(len(links))

        for a in links:
            print(a.text.strip(), "\n")
            # a = post.find('a')            
            # link = urllib.parse.urljoin(post_url, a.get('href').strip())            
            # obj.add_text_task(
            #     unique_key=link,
            #     name=a.text.strip(),
            #     url=link,
            #     data=dict(
            #         title=a.text.strip(),
            #         text=link
            #     )
            # )




