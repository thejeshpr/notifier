import os

import requests

from .TelePusher import TelePusher

UA = os.environ.get('User-Agent')
BASE_URL = os.environ.get('GH_BASE_URL')
GH_TELEGRAM_CHAT_ID = os.environ.get("GH_TELEGRAM_CHAT_ID")

class Gh(object):
    @classmethod
    def send_trending_repos(cls):
        pusher = TelePusher(chat_id=GH_TELEGRAM_CHAT_ID)
        try:
            params = {
                "since": "daily"
            }
            headers = {
                "User-Agent": UA
            }
            res = requests.get(BASE_URL, params=params, headers=headers)
            if res.status_code in [200]:
                msg = []                
                for repo in res.json():                    
                    msg.append(
                            f"{repo['name']}\n"
                            f"{repo['url']}\n"
                            f"{repo.get('description')}\n"
                            f"{repo.get('language')}\n"
                            f"{repo['stars']}\n"                            
                    )                    
                msg = "\n".join(msg)                
        except Exception as e:
            msg = f"Exception: {str(e)}"            
        finally:
            msg = f"GH Stats:\n\n{msg}"            
            pusher.send_message(text=msg)
            