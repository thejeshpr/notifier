from datetime import datetime
import json
import os
import time
import traceback
from typing import Optional, Dict, List, Any
from pprint import pprint
from fastapi import Request
from requests_html import HTMLSession

import requests
from bs4 import BeautifulSoup
import pytz
import telegram
from fastapi.responses import ORJSONResponse

from notifier.db import models
from notifier.db import schema
# from notifier.db import db_cursor
from sqlalchemy.orm import Session
from sqlalchemy import and_

from enum import Enum

class SyncTypeNotFound(Exception):
    # exection class
    pass

class InvalidStatusCode(Exception):
    # exception calss
    pass



class JobStatus(str, Enum):
    COMPLETED = "COMPLETED"
    DISABLED = "DISABLED"
    FAILED = "FAILED"
    PRODUCTIVE = "PRODUCTIVE"    
    STARTED = "STARTED"
    IGNORED = "IGNORED"



class Base(object):
    """
    base class
    """

    def __init__(self, sync_type_name: str, job_id: str, db: Session, request: Request):        
        self.db = db
        self.tasks: List[schema.TaskIn] = []
        self.sync_type = self.get_sync_type(sync_type_name)
        self.job = self.create_job(job_id, request)
        self.request = request
        

    def get_sync_type(self, sync_type_name: str) -> models.SyncType:
        """
        get sync type by name
        """
        res = self.db.query(models.SyncType).filter(models.SyncType.name == sync_type_name).first()

        if not res:
            raise SyncTypeNotFound(f"No SyncType Found with name: {sync_type_name}")
        return res


    def create_job(self, job_id: str, request: Request):
        """
        create job
        """

        if not self.sync_type.enabled:
            status = JobStatus.DISABLED
        elif self.sync_type.locked:
            status = JobStatus.IGNORED
        else:
            status = JobStatus.STARTED

        try:    
            job = models.Job(
                unique_key=job_id,
                sync_type=self.sync_type,
                status=status,
                url=request.url.path,
                qp=Base.parse_qp(request.url.query),
                extras=dict(
                    client_ip=request.client.host,
                    url_path=request.url.path,
                    url_query=Base.parse_qp(request.url.query)
                )
            )
            self.db.add(job)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e
        else:
            self.db.refresh(job)
            return job

    @staticmethod
    def parse_qp(qp: str):
        if not qp:
            return qp
        else:                        
            keys, vals = [], []
            for param in qp.split("&"):
                if param.startswith("xargs_keys="):
                    keys.append(param.replace("xargs_keys=", "").strip())
                elif param.startswith("xargs_vals="):
                    vals.append(param.replace("xargs_vals=", "").strip())

            return ",".join(f"{k}={v}" for k, v in zip(keys, vals))

        
    def is_task_found(self, unique_key: str) -> bool:
        """
        return true task exist
        """
        count = self.db.query(models.Task).filter(models.Task.unique_key == unique_key).count()
        return True if count else False

    def write_tasks(self):
        """
        verify and add task to job
        """                

        # check article extraction required or not
        extract_article = self.sync_type.extras.get("extract_article", False)

        # iterate each task
        for task in self.tasks:
            # check if task not found add it
            if not self.is_task_found(task.unique_key):
                try:
                    task.data["timestamp"] = self.get_current_time()

                    # extract article
                    if extract_article:
                        time.sleep(2)
                        task.data['desc'] = Internet.get_article_data(task.url)

                    self.db.add(
                        models.Task(
                            unique_key=task.unique_key,
                            data=task.data,
                            job=self.job,
                            name=task.name,
                            sync_type=self.sync_type,
                            task_type=task.task_type,
                            url=task.url,
                            args=Base.parse_qp(self.request.url.query)
                        )
                    )
                    self.db.commit()
                    if os.environ.get("DEBUG"):
                        print(task)
                except Exception as e:
                    self.db.rollback()
                    raise e

        self.db.refresh(self.job)  

    def get_current_time(self):
        fmt = "%H:%M-%D"
        utcmoment_naive = datetime.utcnow()        
        utcmoment = utcmoment_naive.replace(tzinfo=pytz.utc)
        tz = os.environ.get("TZ")
        conv_dt = utcmoment.astimezone(pytz.timezone(tz))
        return conv_dt.strftime(fmt)
        

    def add_task(self, task: schema.TaskIn):
        """
        add task to tasks list
        """        
        task.unique_key = f'{self.sync_type.name}:{task.unique_key}'
        self.tasks.append(task)

    def add_text_task(
        self,
        unique_key: str,
        name: str,
        url: str,
        data: Dict[str, Any]
    ):
        """
        add text task to tasks list
        """        
        self.add_task(
            schema.TaskIn(
                unique_key=unique_key,
                data=data,
                name=name,
                task_type=schema.TaskType.message,
                url=url
            )
        )
        

    def add_photo_task(
        self,
        unique_key: str,
        name: str,
        url: str,
        data: Dict[str, Any]
    ):
        """
        add photo task to tasks list
        """        
        self.add_task(
            schema.TaskIn(
                unique_key=unique_key,
                data=data,
                name=name,
                task_type=schema.TaskType.photo,
                url=url
            )
        )
    
    def add_video_task(
        self,
        unique_key: str,
        name: str,
        url: str,
        data: Dict[str, Any]
    ):
        """
        add video task to tasks list
        """        
        self.add_task(
            schema.TaskIn(
                unique_key=unique_key,
                data=data,
                name=name,
                task_type=schema.TaskType.video,
                url=url
            )
        )

    
    def updated_job_status(self, status: str, err: str = None):
        """
        set the task status to fail
        """
        try:
            self.job.status = status
            self.job.err = err
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e
        else:
            self.db.refresh(self.job)


    def job_failed(self):
        """
        set task status to failure
        """
        tb = traceback.format_exc()
        if os.environ.get("DEBUG"): print(tb)        
        self.updated_job_status(status=JobStatus.FAILED, err=tb)

    def job_success(self):
        """
        set task status to success
        """
        self.db.refresh(self.job)
        status = JobStatus.PRODUCTIVE if self.job.tasks else JobStatus.COMPLETED
        self.updated_job_status(status=status)


    def fetch_spaces(self, type: str):
        """
        fetch and returns space objects of given type
        """
        self.db.query(models.Space).filter(models.Space.type == type)


    def get_price_trackers(self) -> List[schema.ProductInfo]:
        """
        fetch and returns price trackes
        """
        return self.db.query(models.PriceTracker).filter(models.PriceTracker.enabled == True)


    def updated_price_tracker(self, product_info: schema.ProductInfo) -> None:
        """
        updated latest product info
        """
        self.db.query(models.PriceTracker).filter(models.PriceTracker.id == product_info.id).\
                    update({
                            models.PriceTracker.curr_price: product_info.curr_price,
                            models.PriceTracker.low_price: product_info.low_price,
                            models.PriceTracker.high_price: product_info.high_price,
                            models.PriceTracker.drop_chance: product_info.drop_chance,
                            models.PriceTracker.avg_price: product_info.avg_price,
                        })

    def change_lock_staus(self, acquire: bool):
        try:
            self.sync_type.locked = acquire
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e
        else:
            self.db.refresh(self.sync_type)

    def lock(self):
        self.change_lock_staus(True)

    def release(self):
        self.change_lock_staus(False)

    def notify(self):
        """
        send notification
        """
        # refresh db objects
        self.db.refresh(self.sync_type)
        self.db.refresh(self.job)

        Notify.send(self.sync_type, self.job.tasks)



class Internet(object):
    """
    class for handling internet activities
    """
    @staticmethod
    def get(
            url: str,            
            params: Dict[str, str] = {},
            headers: Dict[str, str] = None,
            return_json: bool = False,
            use_user_agent: bool = False
        ):
        """
        get html content and return html or json
        """        
        # check is user agent is required
        if use_user_agent:
            headers = headers or dict()
            headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36 Edg/84.0.522.63"

        res = requests.get(url, params=params, headers=headers)
        Internet.check_status_code(res)
        return res.content if not return_json else res.json()

    @staticmethod
    def check_status_code(res):                
        if res.status_code not in [200]:
            if os.environ.get("DEBUG"):
                print(res.content)                
            raise InvalidStatusCode(f"Invalid status code: {res.status_code}\n{res.content}")

    @staticmethod
    def get_soup(
            url: str,            
            params: Dict[str, str] = {},
            headers: Dict[str, str] = None,
            use_user_agent: bool = False
        ):
        """
        returns beautiful soup for html content
        """
        content = Internet.get(url, params=params, headers=headers, use_user_agent=use_user_agent)
        return BeautifulSoup(content, 'html.parser')

    @staticmethod
    def post_phjs(            
            url: str,
            output_as_json: str = "true",
            render_type: str = "plainText",
            return_json:bool = False,
        ):

        # use phantom js to access the content
        data = {
            "url": url,
            "renderType": render_type,
            "outputAsJson": output_as_json
        }        
        
        key = os.environ.get("PHANTOM_KEY")
        url = os.environ.get("PHANTOM_URL").format(key=key)
        res = requests.post(url, data=json.dumps(data))
        Internet.check_status_code(res)        
        return res.content if not return_json else res.json()

    @staticmethod
    def get_soup_phjs(url: str):
        content = Internet.post_phjs(url=url, output_as_json="false", render_type="html")
        return BeautifulSoup(content, 'html.parser')

    @staticmethod
    def post(
            url: str,            
            params: Dict[str, str] = {},
            headers: Dict[str, str] = None,
            data: Dict[str, str] = {},
            return_json: bool = False,
            use_user_agent: bool = False
        ):
        """
        post html content and return html or json
        """        
        # check is user agent is required
        if use_user_agent:
            headers = headers or dict()
            headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36 Edg/84.0.522.63"

        res = requests.post(url, params=params, headers=headers, data=data)
        Internet.check_status_code(res)
        return res.content if not return_json else res.json()

    @staticmethod
    def html_get(
        url: str,            
        params: Dict[str, str] = {},
        headers: Dict[str, str] = None        
    ):
        """
        establish http request
        """
        session = HTMLSession()
        return session.get(url)  


    @staticmethod
    def get_article_data(url: str) -> str:
        """
        returns article of given URL
        """
        api_url = "https://api.diffbot.com/v3/article"
        params = {
            "token": os.environ.get("DIFF_BOT_API_TOKEN"),
            "url": url
        }
        res = requests.get(api_url, params=params)        
        Internet.check_status_code(res)
        return res.json()["objects"][0]["text"]


class Notify(object):
    """
    notify to user
    """
    @staticmethod
    def dispatch(db: Session, sync_type: models.SyncType, limit: int = 10):
        """
        dispatch notification
        """
        tasks = db.query(models.Task)\
                    .join(models.SyncType, sync_type == models.Task.sync_type)\
                        .order_by(models.Task.created_at.asc())\
                            .limit(limit)\
                                .all()

        Notify.send(sync_type, tasks)

    @staticmethod
    def send(sync_type: models.SyncType, tasks: List[models.Task]):
        """
        send notification
        """
        tl = telegram.Bot(token=os.environ.get('TL_BOT_TOKEN'))

        tl_funcs = {
            "message": {
                "func": tl.send_message,
                "params": {
                    "text": "text"
                }
            },
            "photo": {
                "func": tl.send_photo,
                "params": {
                    "caption": "caption",
                    "photo": "url"
                }                 
            },
            "video": {
                "func": tl.send_video,
                "params": {
                    "caption": "caption",
                    "video": "url"
                }
            },            
        }                

        # check if notification dispatch is true
        if sync_type.dispatch_notification == True:
            
            # create dict
            args = dict(chat_id=sync_type.dispatch_to)
            

            # for each tasks
            for task in tasks:
                if os.environ.get("DEBUG"):
                    print(task)
                dispatch_type = task.task_type
                func = tl_funcs[dispatch_type]['func']

                # build args list
                for name, key in tl_funcs[dispatch_type]['params'].items():
                    args[name] = task.data.get(key, "")
                
                # trigger function
                func(**args)
                time.sleep(5)
    

    @staticmethod
    def sync_type_not_found(sync_type_val: str) -> ORJSONResponse:
        return ORJSONResponse(
            content=dict(
                ok=False,
                error=f"No sync type found with name {sync_type_val}"
            ),
            status_code=404
        )

    @staticmethod
    def response_200(info: str) -> ORJSONResponse:
        return ORJSONResponse( content=dict(ok=False, info=info), status_code=200 )

    @staticmethod
    def get_latest_jobs(sync_type_val: str, db: Session, limit: int = 10):
        """
        get the latest jobs of given sync type
        """

        sync_type: models.SyncType = db.query(models.SyncType).filter(models.SyncType.name == sync_type_val).first()
        if not sync_type:
            return Notify.sync_type_not_found(sync_type_val)

        res = db.query(models.Job)\
                .filter(models.Job.sync_type == sync_type)\
                    .order_by(models.Job.created_at.desc())\
                        .limit(10)\
                            .all()        
        return res
    
    @staticmethod
    def get_sync_type_stats(db: Session, return_json=False) -> ORJSONResponse:
        """
        return stats of sync type
        """        
        sync_types: List[models.SyncType] = db.query(models.SyncType).all()
        # print(len(sync_types[0].tasks))

        stats = []

        for sync_type in sync_types:
            stats.append(dict(
                name=sync_type.name,
                id=sync_type.id,
                tasks=db.query(models.Task).filter(models.Task.sync_type == sync_type).count(),
                jobs = db.query(models.Job).filter(models.Job.sync_type == sync_type).count()
            ))

        if return_json:
            return stats
        else:
            return ORJSONResponse(
                content=stats,
                status_code=200
            )        

    
    @staticmethod
    def fe_get_latest_jobs(db: Session):
        """
        return latest jobs
        """
        return db.query(models.Job)\
                .order_by(models.Job.id.desc())\
                    .limit(10)\
                        .all()

    @staticmethod
    def fe_get_latest_tasks(db: Session):
        """
        return latest tasks
        """
        return db.query(models.Task)\
                .order_by(models.Task.id.desc())\
                    .limit(50)\
                        .all()


