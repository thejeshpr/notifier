from notifier.grabbers.base import Base, Internet


class MM(object):    

    @staticmethod
    def sync(obj: Base, *args, **kwargs):
        url = obj.sync_type.base_url
        soup = Internet.get_soup_phjs(url)        

        divs = soup.find_all('div', {'class':'entry-grid-content hgrid-span-12'})
        
        for div in divs[::-1]:

            h2 = div.find("h2", {"class": "entry-title"})
            a = h2.find('a')
            
            url = a.get('href')
            name = a.text.strip()

            desc_div = div.find("div", {"class": "entry-summary"})
            if desc_div:
                desc = desc_div.text.strip()
            
            obj.add_text_task(
                unique_key=url,
                name=name,
                url=url,
                data=dict(text=url, desc=desc)
            )
