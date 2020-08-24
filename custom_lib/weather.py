import os
import requests


class Weather(object):
    def __init__(self, place):        
        self.url = os.environ("WEATHER_URL")
        self.place = os.environ.get("WEATHER_PLACE", place)
        self.app_id = os.environ("WEATHER_APP_ID")
    
    def send_weather_info(self):
        res = requests.get(url)
