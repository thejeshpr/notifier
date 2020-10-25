from notifier import app, templates
from fastapi import Request, Depends, Query
from fastapi.responses import ORJSONResponse, HTMLResponse
# from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from notifier.views.users import User, fastapi_users

from notifier.views import get_db
# from notifier.grabbers.base import Notify
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
    sync_types = db.query(models.SyncType).order_by(models.SyncType.id.desc()).all() 
    return templates.TemplateResponse("sync_types.html", {"items": sync_types, "request": request})


@app.get("/sync-type/{id}", response_class=HTMLResponse)
async def sync_type(
    request: Request,
    id: int,
    db: Session = Depends(get_db),
    user: User = Depends(fastapi_users.get_current_user)
):     
    st = db.query(models.SyncType).filter(models.SyncType.id == id).first()    
    jobs = db.query(models.Job)\
                .filter(models.Job.sync_type == st)\
                    .order_by(models.Job.id.desc())\
                        .limit(10).all()

    tasks = db.query(models.Task)\
                .filter(models.Task.sync_type == st)\
                    .order_by(models.Task.id.desc())\
                        .limit(25).all()    

    return templates.TemplateResponse("sync_type.html", {"sync_type": st, "jobs": jobs, "tasks": tasks, "request": request})


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
    return templates.TemplateResponse("tasks.html", {"items": items, "request": request, "page": page})


@app.get("/job/latest", response_class=HTMLResponse)
async def latest_jobs(
    request: Request,
    db: Session = Depends(get_db),
    page: int = Query(0),
    limit: int = Query(default=25, le=25),
    user: User = Depends(fastapi_users.get_current_user)
):
    request.url_for    
    items = db.query(models.Job)\
                .order_by(models.Job.id.desc())\
                    .offset( limit * page )\
                        .limit(limit)\
                            .all()
    return templates.TemplateResponse("jobs.html", {"items": items, "request": request, "page": page})


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
    return templates.TemplateResponse("job.html", {"job": job, "tasks": tasks, "request": request})
