from typing import List, Optional
from fastapi import APIRouter, Query, BackgroundTasks, Depends
from fastapi.responses import ORJSONResponse
from notifier.db.schema import TaskIn, JobOut
from notifier.db.models import Task, SyncType
from notifier.views import get_db
from sqlalchemy import and_
from sqlalchemy.orm import Session
from notifier.views.options import SyncTypeSet


from notifier.grabbers.base import Notify

router = APIRouter()

@router.get("/{sync_type_val}/latest", response_model=List[TaskIn])
async def get_latest_tasks(
        sync_type_val: SyncTypeSet,
        backgound_tasks: BackgroundTasks,
        db: Session = Depends(get_db),        
        limit: int = Query(10, le=20, gt=0)
    ):
    """
    Send notification of given sync type
    """
    sync_type = db.query(SyncType).filter(SyncType.name == sync_type_val).first()
    if not sync_type:
        return Notify.sync_type_not_found(sync_type_val)

    backgound_tasks.add_task(Notify.dispatch, db, sync_type, limit)

    return Notify.response_200(f"disptched {limit} post of sync type {sync_type_val}")
    

@router.get("/{sync_type}/jobs", response_model=List[JobOut], response_model_exclude=["tasks"])
async def get_latest_jobs(sync_type_val: SyncTypeSet, db: Session = Depends(get_db)):
    """
    return latest tasks
    """    
    return Notify.get_latest_jobs(sync_type_val, db)


@router.get("/stats", response_class=ORJSONResponse)
async def get_stats(db: Session = Depends(get_db)):
    """
    return stats of sync type
    """    
    return Notify.get_sync_type_stats(db)