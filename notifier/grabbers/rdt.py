from notifier.grabbers.base import Base, Internet


class Rdt(object):    

    @staticmethod
    def sync(obj: Base, *args, **kwargs):
        # https://www.reddit.com/
        soup = Internet.get_soup_phjs(obj.sync_type.base_url)
        
        all_cards   = soup.find('div', {'id':'project-grid'})
        posts = all_cards.find_all('div', {'class':['card']})

        for post in posts:
            pid = post.find('div', {'class':'simplefavorite-button has-count'}).get('data-postid').strip()            
            data = {
                'name': post.find("h4", {"class":"card-title"}).text.strip(),
                'url':post.find('a').get('href'),
                # 'download_url': Bfy.get_download_link(obj, pid)
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





