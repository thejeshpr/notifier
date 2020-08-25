import os
import requests


class TelePusher():
    def __init__(self, token=None, chat_id=None):
        self.__token = token or os.environ.get('TELEGRAM_BOT_TOKEN')
        self.__chat_id = chat_id or os.environ.get('TELEGRAM_CHANNEL_ID')
        self.base_url = f"https://api.telegram.org/bot{self.__token}"    
        
    def __dispatch(self, payload: dict, msg_type: str):
        url = f"{self.base_url}/{msg_type}"

        payload['chat_id'] = f"@{self.__chat_id}"
        payload['parse_mode'] = 'markdown'                
        
        return requests.get(url, params=payload).json()
        
    def send_message(self, text: str):
        payload = {            
            "text": text,
            "disable_web_page_preview": "True"
        }
        return self.__dispatch(payload, "sendMessage")
        
    def send_photo(self, photo_url: str, caption=None):
        payload = {            
            "photo": photo_url            
        }

        if caption:
            payload['caption'] = caption

        return self.__dispatch(payload, "sendPhoto")

    def send_video(self, video_url: str, caption=None):
        payload = {            
            "video": video_url            
        }

        if caption:
            payload['caption'] = caption

        return self.__dispatch(payload, "sendVideo")

    def send_document(self, doc_url, caption=None):
        payload = {            
            "photo": doc_url
        }
        
        if caption:
            payload['caption'] = caption

        return self.__dispatch(payload, "sendDocument")