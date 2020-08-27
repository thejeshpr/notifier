import os
import requests
from bs4 import BeautifulSoup
from pprint import pprint
import traceback

from custom_lib.TelePusher import TelePusher

COPRA_TELEGRAM_CHANNEL = os.environ.get("COPRA_TELEGRAM_CHANNEL")

class Copra(object):
    def __init__(self):
        pass # implemet later

    @classmethod
    def send_latest_info(cls):
        try:
            pusher = TelePusher(chat_id=COPRA_TELEGRAM_CHANNEL)
            url = "https://www.krishimaratavahini.kar.nic.in/MainPage/DailyMrktPriceRep2.aspx"
            params = {
                "Rep": "Com",
                "CommCode": "129",
                "VarCode": "1",
                "Date": "05/05/2018",
                "CommName": "Copra / ಕೊಬ್ಬರಿ",
                "VarName": "Copra / ಕೊಬ್ಬರಿ"
            }
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36 Edg/84.0.522.63"
            }
            res = requests.get(url, params=params, headers=headers)
            
            soup = BeautifulSoup(res.content, 'html.parser')
            table = soup.find('table', {'id':'_ctl0_content5_Table1'})        
            header = [td.text.strip() for td in table.find('tr').find_all('td')]
            info = []
            for tr in table.find_all('tr')[1:]:
                row = []
                for head, td in zip(header, tr.find_all('td')):                
                    row.append(f"{head}: {td.text.strip()}")

                info.append("\n".join(row))
            
            msg = "\n\n".join(info)
        except Exception as e:
            msg = f"An error occured: {e}"
            print(traceback.format_exc())
        finally:
            pusher.send_message(text=msg)
        


if __name__ == "__main__":
    Copra.send_latest_info()