import os
import json
import random
import traceback

import requests
from airtable import Airtable

from .TelePusher import TelePusher


class RandomQuote(object):
        
    def __init__(self):
        """
        Initialize
        """
        self.__base_list = os.environ.get("RQ_BASE_LIST")        
        self.__size = None
        self.pusher = TelePusher()
        self.__get_random_base()        

    def __get_random_base(self):
        bases = self.__base_list.split(",")
        rand_num = random.randrange(0, len(bases) - 1)
        base, self.__size = bases[rand_num].split(':')
        self.at = Airtable(base, 'Quotes')

    def get_quote(self):
        try:
            rand_num = random.randrange(0, int(self.__size) - 1)
            formula = '({} = {})'.format('id', rand_num)
            rand_quote = self.at.get_all(formula=formula)[0]['fields']
            quote = rand_quote.get("quoteText")
            author = rand_quote.get("quoteAuthor", "Anonymous")                    
            msg = f"*{quote}*\n--{author}"

            tb = ""

        except Exception as e:
            msg = f"RandomQuote: Error {e}"
            tb = traceback.format_exc()
            msg = "{}\n{}".format(e, tb)

        finally:            
            msg = f"Daily Quote:\n\n{msg}"
            self.pusher.send_message(msg)
