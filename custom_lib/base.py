import time
from typing import Optional, Dict, List

import requests
from bs4 import BeautifulSoup
from airtable import Airtable

from custom_lib import (
    TelePusher,
    AirPost
)


VALID_STATUS_CODE = [200]

class InvalidStatusCode(Exception):
    pass # invalid status code
    

class Base(object):
    """
    base class
    """
    # def __init__(self, ar_base: str, ar_table: str, tl_chat_id:str = None):

    def __init__(self, *args, **kwargs):        
        if kwargs.get("ar_base") and kwargs.get("ar_table"):
            self.ap = AirPost(kwargs.get("ar_base"), kwargs.get("ar_table"))
        self.tl = TelePusher(chat_id=kwargs.get('tl_chat_id'))        
        
            
    def url_get(self, url: str, json:bool = False, params:Dict[str, str] = {}, headers:Dict[str, str] = {}):
        res = requests.get(url, params=params, headers=headers)

        if res.status_code in VALID_STATUS_CODE:
            return res.content if not json else res.json()
        else:
            raise InvalidStatusCode(f"Invalid status code: {res.status_code}")

    def get_soup(self, url):
        content = self.url_get(url)
        return BeautifulSoup(content, 'html.parser')

    
    def tl_send_msg(
                    self,
                    data: List[Dict[str, str]],
                    key: str,
                    interval: int = 1,
                    disable_web_page_preview:str = "False",
                    parse_mode="markdown"):
        """ send msg to tl channel"""

        for info in data:            
            self.tl.send_message(
                text=info[key],
                disable_web_page_preview=disable_web_page_preview,
                parse_mode=parse_mode
            )            
            time.sleep(interval)


