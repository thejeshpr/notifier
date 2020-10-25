from notifier.grabbers.base import Base
from uuid import uuid4
from notifier.db.schema import TaskIn
from sqlalchemy.orm import Session

import requests
from bs4 import BeautifulSoup
from pprint import pprint 
import base64
import time
import json
import os

from notifier.db.schema import ProductInfo

PRICE_TRACKING_BASE_URL = os.environ.get("PRICE_TRACKING_BASE_URL")
ORIGIN = os.environ.get("ORIGIN")
PRICE_TRACKING_URL = os.environ.get("PRICE_TRACKING_URL")


class InvalidProduct(Exception):
    pass # exception for invalid product


class UnableTOProcess(Exception):
    pass # unable to process request


class Tracker(object):

    @staticmethod
    def get_poduct_info(product_url: str):
        """
        get product info
        """
        client = requests.Session()
        res = client.get(PRICE_TRACKING_BASE_URL)        

        auth = base64.b64encode( ("ajax:true-" + str(int(time.time()))).encode("utf-8") )
        auth = "Basic " + str(auth, "utf-8")

        headers = {
            'authority': 'pricehistory.in',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'x-requested-with': 'XMLHttpRequest',  
            'Authorization': auth,
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36 Edg/85.0.564.51',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': ORIGIN,
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': PRICE_TRACKING_BASE_URL,
            'accept-language': 'en-US,en;q=0.9',
            'cookie': f'__cfduid={res.cookies.get("__cfduid")}; _ga=GA1.2.1037178724.1599729668; _gid=GA1.2.2074719493.1601003656; XSRF-TOKEN={res.cookies.get("XSRF-TOKEN")}; _gat_gtag_UA_50001635_52=1; price_history_session={res.cookies.get("price_history_session")}'
        }

        soup = BeautifulSoup(res.content, 'html.parser')
        tkn = soup.find("input", {"name":"_token"}).get("value")

        data = {            
            "product_url": product_url,
            "_token": tkn
        }

        time.sleep(2)
        response = client.post(PRICE_TRACKING_URL, headers=headers, data=data)

        content =  response.json()        
        if content.get("status"):
            content['avg_price'] = content['avg_price'].replace(',','')
            content['curr_price'] = content['curr_price'].replace(',','')
            content['high_price'] = content['high_price'].replace(',','')
            content['low_price'] = content['low_price'].replace(',','')
            return ProductInfo(**content)
        else:
            raise InvalidProduct(content.get("error"))

        
class PriceTrackerSync(object):
    """
    sync the prices
    """
    @staticmethod
    def sync(obj: Base, *args, **kwargs):
        price_trackers = obj.get_price_trackers()
        
        for pt in price_trackers:
            # print("syncing product:", pt.title)
            info = Tracker.get_poduct_info(pt.productUrl)            
            obj.updated_price_tracker(info)
            content = (
                f"Title: {info.title}\n"
                f"Current Price: {info.curr_price}\n"
                f"High Price: {info.high_price}\n"
                f"Low Price: {info.low_price}\n"
                f"URL: {info.productUrl}\n"
            )
            obj.add_text_task(task_id=f"{obj.job.id}:{info.title}", data=dict(text=content))
            # print(f"Synced: {info.title}")
            

