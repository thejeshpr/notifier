from typing import List, Optional, Dict
from fastapi import APIRouter, Query, BackgroundTasks, Depends
from fastapi.responses import ORJSONResponse


from pydantic import BaseModel, HttpUrl
from notifier.grabbers.base import Internet

class UrlTest(BaseModel):
    url: HttpUrl

class UrlTestOut(BaseModel):
    url: HttpUrl    
    status_code: Optional[str] = ''
    headers: Optional[Dict[str, str]] = {}
    body: Optional[str] = ''



from notifier.grabbers.base import Notify

router = APIRouter()

@router.post("/test/")
async def test_url(url_test: UrlTest):
    """
    Test given URL
    """
    try:
        res = Internet.html_get(url_test.url)
        data = UrlTestOut(
            url=url_test.url,
            status_code=res.status_code,
            body=res.content,
            headers=res.headers
        )
    except Exception as e:
        data = str(e)
    return data
