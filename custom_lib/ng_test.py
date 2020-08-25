import requests

from urllib.request import urlopen, Request

def fun():

    url = "https://9gag.com/funny"
    headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}
    # res = requests.get(url, headers=headers)

    req = Request(url=url, headers=headers) 
    html = urlopen(req)

    return  {
        "data": html.read(),
        "code": html.status
    }