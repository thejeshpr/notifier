import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from notifier.db import SessionLocal, db_cursor


SAWWGER_END_POINT = os.environ.get("SAWWGER_END_POINT")
REDOC_END_POINT = os.environ.get("REDOC_END_POINT")
DEBUG = os.environ.get("DEBUG", False)

app = FastAPI(
    title="LoopHoles",
    description="",
    version="2.0",
    docs_url=SAWWGER_END_POINT,
    redoc_url=REDOC_END_POINT
)

@app.on_event("startup")
async def startup():
    """
    initiate db connection when app is started
    """
    await db_cursor.connect()    


@app.on_event("shutdown")
async def shutdown():
    """
    disconnect db connection when app shutdown
    """    
    await db_cursor.disconnect()


# app.mount("/static", StaticFiles(directory="./sparky/static"), name="static")
templates = Jinja2Templates(directory="./notifier/templates")

from notifier.views import main, tasks, users

