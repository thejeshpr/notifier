from notifier import app, templates
from fastapi import Request, Depends, Query
from fastapi.responses import ORJSONResponse, HTMLResponse
from sqlalchemy.orm import Session
from notifier.views.users import User, fastapi_users

from sqlalchemy import func

from notifier.views import get_db
from notifier.db import models


@app.get("/ping")
async def ping():
    return ORJSONResponse(
        content=dict(
            ok=True,
            info="pong"
        ),
        status_code=200
    )


@app.get("/", response_class=HTMLResponse)
async def index(
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(fastapi_users.get_current_user)
):    
    task_sq = db.query(models.Task.sync_type_id, func.count(models.Task.sync_type_id).label('count'))\
            .group_by(models.Task.sync_type_id).subquery()
    job_sq = db.query(models.Job.sync_type_id, func.count(models.Job.sync_type_id).label('count'))\
            .group_by(models.Job.sync_type_id).subquery()

    res = db.query(models.SyncType, job_sq.c.count, task_sq.c.count)\
                .join( 
                        (job_sq, job_sq.c.sync_type_id == models.SyncType.id),
                        (task_sq, task_sq.c.sync_type_id == models.SyncType.id)
                    )\
                    .order_by(models.SyncType.id.asc()).all() 
    context = {
        "items": res,
        "request": request
    }
    return templates.TemplateResponse("sync_types.html", context)


@app.get("/sync-type/{id}", response_class=HTMLResponse)
async def sync_type(
    request: Request,
    id: int,
    db: Session = Depends(get_db),
    user: User = Depends(fastapi_users.get_current_user)
):

    # fetch sync type and stats
    task_sq = db.query(models.Task.sync_type_id, func.count(models.Task.sync_type_id).label('count'))\
            .group_by(models.Task.sync_type_id).subquery()
    job_sq = db.query(models.Job.sync_type_id, func.count(models.Job.sync_type_id).label('count'))\
            .group_by(models.Job.sync_type_id).subquery()

    res = db.query(models.SyncType, job_sq.c.count, task_sq.c.count)\
                .join( 
                        (job_sq, job_sq.c.sync_type_id == models.SyncType.id),
                        (task_sq, task_sq.c.sync_type_id == models.SyncType.id)
                    )\
                    .filter(models.SyncType.id == id)\
                    .first()    

    # fetch jobs and task count
    task_sq = db.query(models.Task.job_id, func.count(models.Task.job_id).label('count'))\
            .group_by(models.Task.job_id).subquery()

    job_res = db.query(models.Job, task_sq.c.count)\
                .join(task_sq, task_sq.c.job_id == models.Job.id)\
                    .filter(models.Job.sync_type_id == id)\
                        .order_by(models.Job.id.desc())\
                            .limit(10)\
                                .all()    

    tasks = db.query(models.Task)\
                .filter(models.Task.sync_type_id == id)\
                    .order_by(models.Task.id.desc())\
                        .limit(25).all()  

    context = {
        "sync_type": res[0],
        "job_count": res[1],
        "task_count": res[2],
        "jobs": job_res,
        "tasks": tasks,
        "request": request,
        "current_page": "Sync Type"
    }  

    return templates.TemplateResponse("sync_type.html", context)


@app.get("/sync-type/{id}/tasks", response_class=HTMLResponse)
async def sync_type_tasks(
    request: Request,
    id: int,
    page: int = Query(0),
    limit: int = Query(default=25, le=25),    
    db: Session = Depends(get_db),
    user: User = Depends(fastapi_users.get_current_user)
):     
    st = db.query(models.SyncType).filter(models.SyncType.id == id).first()
    tasks = db.query(models.Task).filter(models.Task.sync_type == st).order_by(models.Task.id.desc()).offset( limit * page ).limit(25).all()

    context = {
        "sync_type": st,        
        "tasks": tasks,
        "request": request,
        "current_page":"Sync Type Tasks",
        "page": page,
    }

    return templates.TemplateResponse("sync_type_tasks.html", context)


@app.get("/task/latest", response_class=HTMLResponse)
async def latest_tasks(
    request: Request,
    db: Session = Depends(get_db),
    page: int = Query(0),
    limit: int = Query(default=25, le=25),
    user: User = Depends(fastapi_users.get_current_user)
):
    items = db.query(models.Task)\
                .order_by(models.Task.id.desc())\
                    .offset( limit * page )\
                        .limit(limit)\
                            .all()
    return templates.TemplateResponse("tasks.html", {"items": items, "request": request, "page": page, "current_page": "Tasks"})


@app.get("/job/latest", response_class=HTMLResponse)
async def latest_jobs(
    request: Request,
    db: Session = Depends(get_db),
    page: int = Query(0),
    limit: int = Query(default=25, le=25),
    user: User = Depends(fastapi_users.get_current_user)
):
    
    items = db.query(models.Job)\
                .order_by(models.Job.id.desc())\
                    .offset( limit * page )\
                        .limit(limit)\
                            .all()
    return templates.TemplateResponse("jobs.html", {"items": items, "request": request, "page": page, "current_page": "Jobs"})


@app.get("/job/{id}", response_class=HTMLResponse)
async def job(
    request: Request,
    id: int,
    db: Session = Depends(get_db),
    user: User = Depends(fastapi_users.get_current_user)
):     
    job = db.query(models.Job).filter(models.Job.id == id).first()
    tasks = db.query(models.Task)\
                .filter(models.Task.job == job)\
                    .order_by(models.Task.id.desc())\
                        .limit(25).all()
    return templates.TemplateResponse("job.html", {"job": job, "tasks": tasks, "request": request, "current_page": "Job"})


@app.get("/filter/tasks", response_class=HTMLResponse)
def filter_render(
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(fastapi_users.get_current_user)
):    

    filter_params = {

        # ng
        "ng:{nfw:hot}": "ng:group=nsfw,type=hot",
        "ng:{awesome:hot}": "ng:group=awesome,type=hot",        
        "ng:{girl:hot}": "ng:group=girl,type=hot",
        "ng:{girlcelebrity:hot}": "ng:group=girlcelebrity,type=hot",
        "ng:{relationship:hot}": "ng:group=relationship,type=hot",

        # news
        "news": "news",
        "news:{US}": "news:key=country,val=us",

        # weather
        "weather": "weather",
        "weather:{Bangalore}": "weather:city=bangalore",

        # D2
        "d2": "d2",

        # YS
        "ys:{techsparks}": "ys:category=techsparks",
        "ys:{Inspiration}": "ys:category=Inspiration",
        "ys:{Opinion}": "ys:category=Opinion",
        "ys:{Interview}": "ys:category=Interview",
        "ys:{startup}": "ys:category=startup",
        
        # hn
        "hn:{artificial-intelligence}": "hn:tag=artificial-intelligence",
        "hn:{coding}": "hn:tag=coding",
        "hn:{python}": "hn:tag=python",
        "hn:{devops}": "hn:tag=devops",
        "hn:{security}": "hn:tag=security",
        "hn:{gaming}": "hn:tag=gaming",
        "hn:{technology}": "hn:tag=technology",
        "hn:{self-improvement}": "hn:tag=self-improvement",
        "hn:{startups}": "hn:tag=startups",
        "hn:{programming}": "hn:tag=programming",

        # bfy
        "bfy": "bfy",

        # realpython
        "realpython": "realpython",

        # dzone
        "dzone": "dzone",

        # bkdko
        "bkdko": "bkdko",

        # crdko
        "crdko": "crdko",

        # crdko_road_test
        "crdko_road_test": "crdko_road_test",

        # bkdko_road_test
        "bkdko_road_test": "bkdko_road_test",

        # autocrind
        "autocrind": "autocrind",

        # crwle
        "crwle": "crwle",
    }

    return templates.TemplateResponse(
        "task-filter.html",
        {
            "filter_params": filter_params,
            "request": request,
            "current_page": "filters-task"
        }
    )


def parse_params(param: str) -> dict:
    if ":" in param:
        params = param.split(":")
        sync_type, qp = params[0], params[1]
    else:
        sync_type, qp = param, None
    
    return {
        "sync_type": sync_type,
        "qp": qp
    }


# def get_tasks_count(param: str):
#     params = parse_params(param)
#     sync_type = db.query(models.SyncType)\
#                     .filter(models.SyncType.name == param["sync_type"])\                        
#                         .first()
#     tasks = db.query(models.Task)\
#                 .join(models.SyncType, models.SyncType == sync_type)\
#                     .join(models.Job, models.Job. == sync_type)

# app.get("/filter/{params}", response_class=HTMLResponse)
# def parse_filter(
#     request: Request,
#     db: Session = Depends(get_db),
#     user: User = Depends(fastapi_users.get_current_user)
# ):
#     # pass