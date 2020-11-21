import datetime
import os
from uuid import uuid4

from notifier.grabbers.base import Base, Internet


class Weather(object):    

    @staticmethod
    def sync(obj: Base, *args, **kwargs):
        city = kwargs.get('city') or os.environ.get("WEATHER_DEFAULT_CITY")
        url = obj.sync_type.base_url
        params = {
            "units": "metric",
            "q": city,
            "APPID": os.environ.get('WEATHER_API_KEY')
        }
        data = Internet.get(url=url, return_json=True, params=params)
        
        # data["text"] = (
        #     f"city: {city}\n"
        #     f"temp: {data['main']['temp']}\n"
        #     f"feels like: {data['main']['feels_like']}\n"
        #     f"temp min: {data['main']['temp_min']}\n"
        #     f"temp_max: {data['main']['temp_max']}\n"
        #     f"pressure: {data['main']['pressure']}\n"
        #     f"humidity: {data['main']['humidity']}\n"
        #     f"visibility: {data['visibility']}\n"
        #     f"wind speed: {data['wind']['speed']}\n"
        #     f"weather: {data['weather'][0]['main']} ({data['weather'][0]['description']})\n"
        #     f"sunrise: {datetime.datetime.fromtimestamp(data['sys']['sunrise']).isoformat()}\n"
        #     f"sunset: {datetime.datetime.fromtimestamp(data['sys']['sunset']).isoformat()}\n"
        # )
        icon_url = f"http://openweathermap.org/img/wn/{data['weather'][0]['main']}@2x.png"
        img_tag = f'<img src="{icon_url}" class="img-fluid" alt="Responsive image">'
        temp_data = f"{data['main']['temp']} (feels like: {data['main']['feels_like']}), {data['weather'][0]['description']}"

        obj.add_text_task(
            unique_key=str(uuid4()),
            name=f"{city}: {temp_data}",
            url=obj.sync_type.extras.get("weather_url").format(city_id=data['id']),
            data=data
        )

