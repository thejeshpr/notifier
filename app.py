import os
import time
from typing import Optional

from fastapi import BackgroundTasks, FastAPI

from custom_lib import buildofy, response_handler, random_quote

app = FastAPI()
res = response_handler.Response
Buildofy = buildofy.Buildofy
RandomQuote = random_quote.RandomQuote

SAWWGER_END_POINT = os.environ.get("SAWWGER_END_POINT")
REDOC_END_POINT = os.environ.get("REDOC_END_POINT")

app = FastAPI(docs_url=SAWWGER_END_POINT, redoc_url=REDOC_END_POINT)

@app.get("/")
def read_root(background_tasks: BackgroundTasks):        
    background_tasks.add_task(Buildofy.sync, os.environ.get("B_BOX_ID"))    
    return res("Welcome")


@app.get("/sync-b")
async def sync_b(background_tasks: BackgroundTasks):        
    background_tasks.add_task(Buildofy.sync, os.environ.get("B_BOX_ID"))    
    return res("sync job initiated")
    

@app.get("/sleep/{seconds}")
async def sleep(seconds: int, background_tasks: BackgroundTasks):    
    background_tasks.add_task(sleep, seconds)    
    return res(f"sleeping for {seconds} seconds")


def sleep(seconds):
    time.sleep(seconds)
    print(f"{seconds} done")


@app.get("/ping")
def ping():
    return res("pong")


@app.get("/link/{post_id}")
def get_link(post_id: int):    
    return res(Buildofy.get_download_link(post_id))


@app.get("/random-quote")
async def random_quote(background_tasks: BackgroundTasks):
    rquote = RandomQuote()
    background_tasks.add_task(rquote.get_quote)
    return res(f"random quote dispatched")