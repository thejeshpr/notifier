import os
import time
import traceback
from pprint import pprint

from airtable import Airtable
from newsapi import NewsApiClient

from .TelePusher import TelePusher


class News():
    def __init__(self):
        self.__key = os.environ.get("NEWS_API_KEY")
        self.__client = NewsApiClient(api_key=self.__key)                
        self.at = Airtable('app6DJobATJinSLqX', 'articles')
        self.pusher = TelePusher(chat_id=os.environ.get("TELEGRAM_NEWS_CHANNEL"))        


    def send_latest_news(self, country="us"):
        try:            
            top_headlines = self.__client.get_top_headlines(language="en", country=country)
            records = self.at.get_all()
            existing_articles = [record.get('fields').get('url') for record in records]
            fetched_articles = [article.get('url') for article in top_headlines.get('articles')]
            new_articles = list(set(fetched_articles) - set(existing_articles))            

            self.pusher.send_message(f"{len(new_articles)} article(s) found")
            
            for article in new_articles:
                self.pusher.send_message(text=article)
                self.at.insert({'url': article})
                time.sleep(5)

        except Exception as e:
            msg = f"NewsApi: Error\n{e}\n{traceback.format_exc()}"            
            self.pusher.send_message(text=msg)

    def clean_up(self):
        try:
            threshold = os.environ.get("ARTILCE_CLEAN_UP_THRESHOLD", 3)                        
            formula = f"( DATETIME_DIFF(TODAY(), CREATED_TIME(), 'days') >= {threshold})"
            records = self.at.get_all(formula=formula)

            if records:
                articles_to_rmv = [rec.get('id') for rec in records]                        
                self.at.batch_delete(articles_to_rmv)
                
            msg = f"{len(records)} articles has been removed"
            error = False
        except Exception as e:
            error = True
            msg = f"Error\n{e}\n{traceback.format_exc()}"
            
        finally:
            status = "Succes" if not error else "Failure"
            msg = f"News Clean-up: {status}\n\n{msg}"
            self.pusher.send_message(text=msg)
