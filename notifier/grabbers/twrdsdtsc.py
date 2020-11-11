import urllib.parse
from notifier.grabbers.base import Base, Internet


class Twrdsdtsc(object):    

    @staticmethod
    def sync(obj: Base, *args, **kwargs):
                
        r = Internet.html_get(obj.sync_type.base_url)
        links = r.html.xpath('/html/body/div/div/div[3]/div/div[2]/div/div[*]/div/div/div/div[1]/div[2]/div/section/div/h1/a')
        
        for a in links[::-1]:            
            url = urllib.parse.urljoin(obj.sync_type.base_url, a.attrs.get('href'))
            name = a.text.strip()            

            obj.add_text_task(
                unique_key=url,
                name=name,
                url=url,
                data=dict(text=url)
            )

    # @staticmethod
    # def sync(obj: Base, *args, **kwargs):
        
    #     # soup = Internet.get_soup_phjs("https://ahmed-nafies.medium.com/")
    #     # links = soup.find_all('a', {'class':'ec br'})        
    #     # links = soup.find_all('a', {'class':'dl bn'})

    #     r = Internet.request_js_get("https://ahmed-nafies.medium.com/")
    #     links = r.html.xpath('/html/body/div/div/div[3]/div/div[2]/div/div[*]/div/div/div/div[1]/div[2]/div/section/div/h1/a')
        
    #     for a in links[::-1]:            
    #         url = urllib.parse.urljoin(obj.sync_type.base_url, a.get('href'))
    #         name = a.text.strip()
    #         print(url, name)

    #         obj.add_text_task(
    #             unique_key=url,
    #             name=name,
    #             url=url,
    #             data=dict(text=url)
    #         )

    # @staticmethod
    # def sync(obj: Base, *args, **kwargs):
        
    #     # soup = Internet.get_soup_phjs("https://medium.com/better-advice")
    #     # links = soup.find_all('a', {'class':'ec br'})        
    #     # divs = soup.find_all('div', {'class':'col u-xs-marginBottom10 u-paddingLeft0 u-paddingRight0 u-paddingTop15 u-marginBottom30'})
        
    #     r = Internet.request_js_get("https://medium.com/better-advice")
    #     links = r.html.xpath('/html/body/div/div/div[3]/div/div[2]/div/div[*]/div/div/div/div[1]/div[2]/div/section/div/h1/a')

    #     for div in divs[::-1]:            
    #         a = div.find('a')
    #         url = urllib.parse.urljoin(obj.sync_type.base_url, a.get('href'))
    #         h3 = a.find('h3')
    #         name = h3.text.strip()
    #         print(url, name)

    #         obj.add_text_task(
    #             unique_key=url,
    #             name=name,
    #             url=url,
    #             data=dict(text=url)
    #         )


    # @staticmethod
    # def sync(obj: Base, *args, **kwargs):
        
    #     soup = Internet.get_soup_phjs("https://medium.com/in-fitness-and-in-health")
    #     # links = soup.find_all('a', {'class':'ec br'})        
    #     divs = soup.find_all('div', {'class':'col u-xs-marginBottom10 u-paddingLeft0 u-paddingRight0 u-paddingTop15 u-marginBottom30'})
        
    #     for div in divs[::-1]:            
    #         a = div.find('a')
    #         url = urllib.parse.urljoin(obj.sync_type.base_url, a.get('href'))
    #         h3 = a.find('h3')
    #         name = h3.text.strip()
    #         print(url, name)

    #         obj.add_text_task(
    #             unique_key=url,
    #             name=name,
    #             url=url,
    #             data=dict(text=url)
    #         )
    
    # @staticmethod
    # def sync(obj: Base, *args, **kwargs):
        
    #     soup = Internet.get_soup_phjs("https://psiloveyou.xyz/")
    #     # links = soup.find_all('a', {'class':'ec br'})        
    #     links = soup.find_all('a', {'class':'u-block u-sizeFull u-backgroundSizeCover u-backgroundOriginBorderBox u-borderLighter u-borderBox u-backgroundColorGrayLight'})
    #     print(links)
        
    #     for a in links[::-1]:            
    #         url = urllib.parse.urljoin(obj.sync_type.base_url, a.get('href'))
    #         span = a.find('span')
    #         name = span.text.strip()
    #         print(url, name)

    #         obj.add_text_task(
    #             unique_key=url,
    #             name=name,
    #             url=url,
    #             data=dict(text=url)
    #         )

    # @staticmethod
    # def sync(obj: Base, *args, **kwargs):
        
    #     soup = Internet.get_soup_phjs("https://medium.com/knowledge-stew")
    #     # links = soup.find_all('a', {'class':'ec br'})        
    #     links = soup.find_all('a', {'class':'ec bt'})        
    #     print(links)
    #     for a in links[::-1]:            
    #         url = urllib.parse.urljoin(obj.sync_type.base_url, a.get('href'))
    #         name = a.text.strip()

    #         obj.add_text_task(
    #             unique_key=url,
    #             name=name,
    #             url=url,
    #             data=dict(text=url)
    #         )


# r.html.xpath('/html/body/div/div/div[*]/div[*]/div/div[*]/div/div/div/div[1]/div[2]/div/section/div/h1/a')