import requests
from .models import Payload

def fire_get(payload: Payload):
    data = {}
    try:
        res = requests.get(payload.url, headers=payload.headers, params=payload.params)
        data['success'] = True
        data['status_code'] = res.status_code

        content_type = res.headers.get("Content-Type")
        if "application/json" in content_type:
            content = res.json()
        else:
            content = res.content

        data['content'] = content

    except Exception as e:
        data['success'] = False
        data['error'] = str(e)        
    return data
    