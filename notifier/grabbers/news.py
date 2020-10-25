import os

from newsapi import NewsApiClient

from notifier.grabbers.base import Base, Internet


class News(object):    

    @staticmethod
    def sync(obj: Base, *args, **kwargs):

        client = NewsApiClient(api_key=os.environ.get('NEWS_API_KEY'))        
        # countries https://github.com/mattlisiv/newsapi-python/blob/master/newsapi/const.py
        country = kwargs.get("country", "in")
        top_headlines = client.get_top_headlines(language="en", country=country)
        
        articles = top_headlines.get('articles')[::-1]

        for article in articles:
            article['text'] = article['url']
            obj.add_text_task(
                unique_key=article.get("url"),
                name=article['title'],
                url=article['url'],
                data=article
            )
    
