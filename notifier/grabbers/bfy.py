from notifier.grabbers.base import Base, Internet


class Bfy(object):

    @staticmethod
    def get_download_link(obj: Base, pid: str):
        download_endpoint = obj.sync_type.extras.get("download_endpoint")
        return f"{obj.sync_type.base_url}{download_endpoint}{pid}"       

    @staticmethod
    def sync(obj: Base, *args, **kwargs):

        # define number of posts to check
        # no_of_posts = int(kwargs.get("no_of_posts", 10))
        
        soup = Internet.get_soup_phjs(obj.sync_type.base_url)
        
        all_cards   = soup.find('div', {'id':'project-grid'})
        posts = all_cards.find_all('div', {'class':['card']})[::-1]

        for post in posts:
            pid = post.find('div', {'class':'simplefavorite-button has-count'}).get('data-postid').strip()            
            data = {
                'name': post.find("h4", {"class":"card-title"}).text.strip(),
                'url':post.find('a').get('href'),
                'download_url': Bfy.get_download_link(obj, pid)
            }
            data["text"] = (
                        f"Name: {data.get('name')}\n"
                        f"URL: {data.get('url')}\n"
                        f"Link: {data.get('download_url')}\n"
                    )
            
            obj.add_text_task(
                unique_key=pid,
                name=data['name'],
                url=data['url'],
                data=data
            )





