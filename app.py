import os
import time
from typing import Optional

from fastapi import BackgroundTasks, FastAPI

from custom_lib import (
    Bfy,
    Response,
    RandomQuote,
    Covid19)

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


@app.get("/covid-19")
async def covid_19(background_tasks: BackgroundTasks):
    c19 = Covid19()
    background_tasks.add_task(c19.get_stats)
    return res(f"information dispatched")