import os

from notifier import app, templates
from fastapi import Request, Depends, Query
from fastapi.responses import ORJSONResponse, HTMLResponse
from sqlalchemy.orm import Session
from notifier.views.users import User, fastapi_users

from sqlalchemy import func, and_

from notifier.views import get_db
from notifier.db import models

from datetime import datetime, timedelta, date
import base64 


DATE_FORMAT = "%Y-%m-%d"

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


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(
    request: Request,
    day: int = Query(None, ge=1, le=31),
    month: int = Query(None, ge=1, le=12),
    year: int = Query(None, ge=2020, le=2037),
    db: Session = Depends(get_db),    
    user: User = Depends(fastapi_users.get_current_user)
    ):
    if day and month and year:
        from_date = datetime(year, month, day)
    else:
        from_date = datetime(datetime.today().year, datetime.today().month, datetime.today().day)
    

    # from_date = from_date - timedelta(hours=7, minutes=26)
    # from_date = get_current_time(from_date)
    # print("------------------------------") 
    # print(from_date, "-", to_date)
    # print(get_current_time(from_date))

    to_date = from_date + timedelta(days=1)   
    
    task_sq = db.query(models.Task.sync_type_id, func.count(models.Task.sync_type_id).label('count'))\
            .filter(and_(
                models.Task.created_at >= from_date,
                models.Task.created_at <= to_date,
            ))\
            .group_by(models.Task.sync_type_id).subquery()

    job_sq = db.query(models.Job.sync_type_id, func.count(models.Job.sync_type_id).label('count'))\
            .filter(and_(
                models.Job.created_at >= from_date,
                models.Job.created_at <= to_date,
            ))\
            .group_by(models.Job.sync_type_id).subquery()

    res = db.query(models.SyncType, task_sq.c.count, job_sq.c.count)\
                .outerjoin(
                    (job_sq, job_sq.c.sync_type_id == models.SyncType.id),
                    (task_sq, task_sq.c.sync_type_id == models.SyncType.id)
                    )\
                    .order_by(task_sq.c.count.desc()).all() 

    from_dt = f"{from_date.day}/{from_date.month}/{from_date.year}"
    to_dt = f"{to_date.day}/{to_date.month}/{to_date.year}"

    # sort items by count
    sorted_items = sorted(res, key=lambda x:x[1] if x[1] else 0, reverse=True)
    
    count = 0

    for r in res:
        if r[1]:
            count = count + int(r[1])

    context = {
        "items": sorted_items,
        "from_dt": from_dt,
        "to_dt": to_dt,
        "days": range(1,32),
        "months": range(1,13),
        "years": range(2020,2022),
        "selected_day": from_date.day,
        "selected_month": from_date.month,
        "selected_year": from_date.year,
        "current_page": "Dashboard",
        "from_date": from_date.strftime(DATE_FORMAT),
        "to_date": to_date.strftime(DATE_FORMAT),
        "task_count": count,
        "request": request
    }    
    return templates.TemplateResponse("dashboard.html", context)

    



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

    # fetch jon and task count
    job_res = db.query(models.Job, func.count(models.Task.id)).filter(models.Job.sync_type_id == id).\
                outerjoin(models.Task).\
                    group_by(models.Job.id).\
                        order_by(models.Job.id.desc()).\
                            limit(10).all()    

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

    # fetch tasks
    tasks = db.query(models.Task).filter(models.Task.sync_type_id == id)\
                .order_by(models.Task.id.desc())\
                    .offset( limit * page )\
                        .limit(25)\
                            .all()

    context = {
        "sync_type": res[0],
        "job_count": res[1],
        "task_count": res[2],
        "tasks": tasks,
        "request": request,
        "current_page":"Sync Type Tasks",
        "page": page,
    }

    return templates.TemplateResponse("sync_type_tasks.html", context)


@app.get("/sync-type/{id}/tasks-by-date/{from_date}/{to_date}", response_class=HTMLResponse)
async def sync_type_tasks_by_date(
    request: Request,
    id: int,
    from_date: date,
    to_date: date,
    page: int = Query(0),
    limit: int = Query(default=25, le=25),    
    db: Session = Depends(get_db),
    user: User = Depends(fastapi_users.get_current_user)
    ):         

    
    task_sq = db.query(models.Task.sync_type_id, func.count(models.Task.sync_type_id).label('count'))\
            .filter(and_(
                models.Task.created_at >= from_date,
                models.Task.created_at <= to_date
            ))\
            .group_by(models.Task.sync_type_id).subquery()
        
    job_sq = db.query(models.Job.sync_type_id, func.count(models.Job.sync_type_id).label('count'))\
            .filter(and_(
                models.Job.created_at >= from_date,
                models.Job.created_at <= to_date,
            ))\
            .group_by(models.Job.sync_type_id).subquery()

    res = db.query(models.SyncType, job_sq.c.count, task_sq.c.count)\
                .join( 
                        (job_sq, job_sq.c.sync_type_id == models.SyncType.id),
                        (task_sq, task_sq.c.sync_type_id == models.SyncType.id)
                    )\
                    .filter(models.SyncType.id == id)\
                        .first()

    # fetch tasks
    tasks = db.query(models.Task).filter(models.Task.sync_type_id == id)\
            .filter(and_(
                    models.Task.created_at >= from_date,
                    models.Task.created_at <= to_date
                ))\
                .order_by(models.Task.id.desc())\
                    .offset( limit * page )\
                        .limit(25)\
                            .all()

    context = {
        "sync_type": res[0],
        "job_count": res[1],
        "task_count": res[2],
        "tasks": tasks,
        "request": request,
        "current_page":"ST by Date",
        "from_date": from_date.strftime(DATE_FORMAT),
        "to_date": to_date.strftime(DATE_FORMAT),
        "page": page,
    }

    return templates.TemplateResponse("sync_type_tasks_by_date.html", context)


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
    context = {
        "items": items,
        "request": request,
        "page": page,
        "current_page": "Tasks"
    }
    return templates.TemplateResponse("tasks.html", context)


@app.get("/job/latest", response_class=HTMLResponse)
async def latest_jobs(
    request: Request,
    db: Session = Depends(get_db),
    page: int = Query(0),
    limit: int = Query(default=25, le=25),
    user: User = Depends(fastapi_users.get_current_user)
    ):
    job_res = db.query(models.Job, func.count(models.Task.id)).\
                outerjoin(models.Task).\
                    group_by(models.Job.id).\
                        order_by(models.Job.id.desc()).\
                            offset( limit * page ).\
                                limit(limit).all()    

    context = {
        "items": job_res,
        "request": request,
        "page": page,
        "current_page": "Jobs"
    }
    return templates.TemplateResponse("jobs.html", context)


@app.get("/job/{id}", response_class=HTMLResponse)
async def job(
    request: Request,
    id: int,
    db: Session = Depends(get_db),
    user: User = Depends(fastapi_users.get_current_user)
    ):    

    job_res = db.query(models.Job, func.count(models.Task.id)).filter(models.Job.id == id).\
                outerjoin(models.Task).\
                    group_by(models.Job.id).first()
    
    tasks = db.query(models.Task)\
                .filter(models.Task.job_id == id)\
                    .order_by(models.Task.id.desc())\
                        .limit(25).all()
    
    context = {
        "job": job_res[0],
        "task_count": job_res[1],
        "tasks": tasks,
        "request": request,
        "current_page": "Job"
    }
    return templates.TemplateResponse("job.html", context)


@app.get("/bookmark/{id}", response_class=ORJSONResponse)
async def bookmark(
        request: Request,
        id: int,
        db: Session = Depends(get_db),
        user: User = Depends(fastapi_users.get_current_user)
    ): 

    task = db.query(models.Task).filter(models.Task.id == id).first()
    if task:
        task.bookmark = True
        db.commit()
        return ORJSONResponse(
            content=dict(ok=True, message="bookmarked", title=task.name, id=id),
            status_code=200
        )
    else:
        return ORJSONResponse(
            content=dict(ok=False, message=f"No task found with id {id}"),
            status_code=404
        )


@app.get("/bookmarks", response_class=HTMLResponse)
async def bookmarks(
    request: Request,
    db: Session = Depends(get_db),
    page: int = Query(0),
    limit: int = Query(default=25, le=25),
    user: User = Depends(fastapi_users.get_current_user)
    ):
    items = db.query(models.Task)\
                .filter(models.Task.bookmark == True)\
                    .order_by(models.Task.id.desc())\
                        .offset( limit * page )\
                            .limit(limit)\
                                .all()
    context = {
        "items": items,
        "request": request,
        "page": page,
        "current_page": "Bookmarks"
    }
    return templates.TemplateResponse("tasks.html", context)

    


@app.get("/filter/tasks", response_class=HTMLResponse)
def filter_render(
        request: Request,
        db: Session = Depends(get_db),
        user: User = Depends(fastapi_users.get_current_user)
    ):

    stats_sq = db.query(
                    models.Task.args.label('args'),
                    models.Task.sync_type_id.label('sync_type_id'),
                    func.count(models.Task.sync_type_id).label('count')
                )\
                .group_by(models.Task.sync_type_id, models.Task.args)\
                    .subquery()
                    
    res = db.query(models.SyncType, stats_sq.c.args, stats_sq.c.count)\
                    .join(stats_sq, stats_sq.c.sync_type_id == models.SyncType.id)\
                        .order_by(models.SyncType.name)\
                            .all() 

    data = []

    for sync_type, args, count in res:
        arg = args or 'default'
        arg_bytes = arg.encode('ascii')
        encoded_data = base64.b64encode(arg_bytes)
        data.append(
            (sync_type, args, count, encoded_data.decode('ascii'))
        )
    
    context = {
        "stats": data,
        "request": request,
        "current_page": "filters-task"
    }

    return templates.TemplateResponse("task-filter.html", context=context)



@app.get("/filter/tasks/{id}/{arg}", response_class=HTMLResponse)
def parse_filter(
        request: Request,
        id: int,
        arg: str,
        page: int = Query(0),
        limit: int = Query(default=25, le=25),
        db: Session = Depends(get_db),
        user: User = Depends(fastapi_users.get_current_user)
    ):

    base64_bytes = arg.encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    decoded_arg = message_bytes.decode('ascii')    

    decoded_arg = '' if decoded_arg == 'default' else decoded_arg
    
    tasks = db.query(models.Task)\
                .filter(
                    and_(
                        models.Task.args == decoded_arg,
                        models.Task.sync_type_id == id
                    )
                )\
                .order_by(models.Task.id.desc())\
                    .offset( limit * page )\
                        .limit(limit)\
                            .all()
    context = {
        "items": tasks,
        "request": request,
        "encoded_data": arg,
        "sync_type_id": id,
        "page": page,
        "current_page": "Tasks-filtered"        
    }
    return templates.TemplateResponse("tasks-by-arg.html", context)

