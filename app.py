import os
import time
from typing import Optional
from uuid import uuid4

from fastapi import BackgroundTasks, FastAPI

from custom_lib import (
    Bfy,
    Covid19,
    News,
    RandomQuote,
    Response,    
    Unsplash
    )

app = FastAPI()
res = Response

SAWWGER_END_POINT = os.environ.get("SAWWGER_END_POINT")
REDOC_END_POINT = os.environ.get("REDOC_END_POINT")

app = FastAPI(docs_url=SAWWGER_END_POINT, redoc_url=REDOC_END_POINT)

@app.get("/")
def read_root():    
    return res("Welcome")


@app.get("/ping")
def ping():
    return res("pong")


@app.get("/sync-b")
async def sync_b(background_tasks: BackgroundTasks):
    bfy = Bfy()
    background_tasks.add_task(bfy.sync)
    return res("sync job initiated")
    

@app.get("/sleep/{seconds}")
async def sleep(seconds: int, background_tasks: BackgroundTasks):    
    background_tasks.add_task(sleep, seconds)    
    return res(f"sleeping for {seconds} seconds")


def sleep(seconds):
    time.sleep(seconds)
    print(f"{seconds} done")


@app.get("/random-quote")
async def random_quote(background_tasks: BackgroundTasks):
    rquote = RandomQuote()
    background_tasks.add_task(rquote.get_quote)
    return res(f"random quote dispatched")

@app.get("/random-image")
async def random_image(background_tasks: BackgroundTasks):
    uid = str(uuid4())
    rimg = Unsplash()
    background_tasks.add_task(rimg.send_random_image, uid)
    return res(f"random image dispatched {uid}")


@app.get("/covid-19")
async def covid_19(background_tasks: BackgroundTasks):
    c19 = Covid19()
    background_tasks.add_task(c19.get_stats)
    return res(f"information dispatched")

@app.get("/latest-news")
async def latest_news(background_tasks: BackgroundTasks, c: Optional[str] = None):    
    na = News()
    if c:
        background_tasks.add_task(na.send_latest_news, c)
    else:
        background_tasks.add_task(na.send_latest_news)
    return res(f"information dispatched")

@app.get("/news-clean-up")
async def news_clean_up(background_tasks: BackgroundTasks):
    na = News()
    background_tasks.add_task(na.clean_up)
    return res(f"task initiated")