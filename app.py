import os
import time
from typing import Optional

from fastapi import BackgroundTasks, FastAPI

from custom_lib import buildofy, response_handler

app = FastAPI()
res = response_handler.Response
Buildofy = buildofy.Buildofy


@app.get("/")
async def read_root(background_tasks: BackgroundTasks):        
    background_tasks.add_task(Buildofy.sync, os.environ.get("B_BOX_ID"))    
    return res("sync job initiated")    
    

@app.get("/sleep/{seconds}")
async def read_root(seconds: int, background_tasks: BackgroundTasks):    
    background_tasks.add_task(sleep, seconds)    
    return res(f"sleeping for {seconds} seconds")


def sleep(seconds):
    time.sleep(seconds)
    print(f"{seconds} done")


@app.get("/ping")
def read_item():
    return res("pong")


@app.get("/link/{post_id}")
def get_link(post_id: int):    
    return res(Buildofy.get_download_link(post_id))
        