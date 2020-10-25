from notifier.grabbers.base import Base, Internet


class DSRCourse(object):    

    @staticmethod
    def sync(obj: Base, *args, **kwargs):            
        soup = Internet.get_soup(obj.sync_type.base_url)
        ul = soup.find('ul', {'id':'posts-container'})

        for li in ul.find_all('li')[::-1]:
            data = {
                "text": li.find('h3').find('a').get('href').strip(),
                "title": li.find('h3').find('a').text.strip()
            }             

            obj.add_text_task(
                unique_key=data['text'],
                name=data['title'],
                url=data['text'],
                data=data
            )

