from typing import List, Optional

from fastapi import APIRouter, Query, BackgroundTasks, Depends, Request
from fastapi.responses import ORJSONResponse, JSONResponse
from sqlalchemy.orm import Session

# from notifier.db import db_cursor
from notifier.db.models import SyncType, Task
from notifier.db.schema import SyncTypeIn, SyncTypeOut, SyncTypeList
from notifier.views import get_db
from notifier.views.options import SyncTypeSet
from notifier.grabbers import Sync



class SyncTypeCrud(object):
    """
    class for pricetracker crud operations
    """
    @classmethod
    def create(cls, payload: SyncTypeIn, db: Session) -> SyncType:
        """
        create new price tracker
        """
        # check if already exist
        count = db.query(SyncType).filter(SyncType.name == payload.name).count()
        if count:
            return SyncTypeCrud.response_already_exist(payload.name)
        
        obj = SyncType(**payload.dict())
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj
    
    @classmethod
    def search(cls, name: str, limit: int, page: int, db: Session) -> List[SyncType]:
        """
        search for product by name
        """
        return db.query(SyncType)\
                .filter(SyncType.name.contains(name))\
                .limit(limit).offset(page * limit)\
                .all()

    @classmethod
    def list_all(cls, limit: int, page: int, db: Session) -> List[SyncType]:
        """
        list all pricetraker
        """
        return db.query(SyncType).limit(limit).offset(page * limit).all()

    @classmethod
    def get(cls, id: str, db: Session) -> SyncType:
        """
        returns pricetracker by id
        """
        obj = db.query(SyncType).filter(SyncType.id == id).first()
        if obj:
            return obj
        else:
            return SyncTypeCrud.response_404(id)

    @classmethod
    def update(cls, id: int, payload: SyncTypeIn, db: Session) -> dict:
        """
        update the sync type
        """
        res = db.query(SyncType).filter(SyncType.name == payload.name).first()

        # check if already exist
        if res and id != res.id :
            return SyncTypeCrud.response_already_exist(payload.name)

        db.query(SyncType).filter(SyncType.id == id ).update(values=payload.dict())
        db.commit()
        return dict(id=id, **payload.dict())

    @classmethod
    def delete(cls, id: str, db: Session) -> ORJSONResponse:
        """
        delete pricetracker by id
        """
        count = db.query(SyncType).filter(SyncType.id == id).delete()        
        db.commit()
        if not count:
            return SyncTypeCrud.response_404(id)
        else:
            return SyncTypeCrud.response_200(f"Deleted Item with id {id}")

    @classmethod
    def change_state(cls, id: str, state: bool, db: Session) -> SyncType:
        """
        update tracker enabled state and return item
        """
        obj = db.query(SyncType).filter(SyncType.id == id).first()        
        if obj:
            obj.enabled = state
            db.commit()
            return obj
        else:
            return SyncTypeCrud.response_404(id)

    @classmethod
    def change_all_state(cls, key, state: bool, db: Session) -> ORJSONResponse:
        """
        change enabled state of all sync type
        """
        db.query(SyncType).update({key: state})
        db.commit()
        count = db.query(SyncType).count()
        return SyncTypeCrud.response_200(f"{count} sync types state changed to {state}")        

    @classmethod
    def response_404(cls, id: str) -> ORJSONResponse:
        """
        return JSON response
        """
        return ORJSONResponse(
                content=dict(
                    ok=False,
                    error=f"No items found with id {id}"
                ),
                status_code=404
            )
    
    @classmethod
    def response_200(cls, info: str) -> ORJSONResponse:
        """
        return JSON response
        """
        return ORJSONResponse( content=dict( ok=True, info=info ) )
    
    @classmethod
    def response_already_exist(cls, name: str) -> ORJSONResponse:
        """
        return ORJSON respone
        """
        return ORJSONResponse(
                content=dict(
                    ok=False,
                    error=f"Item already exist with given name f{name}"
                ),
                status_code=403
            )



router = APIRouter()

sync_type_exclude_list = [
        "dispatch_key",        
        "disable_parse_web",
        "dispatch_type",
        "time_aware_dispatch",        
    ]


# @router.get("/", response_model=List[SyncTypeList], response_model_exclude=sync_type_exclude_list)
@router.get("/", response_model=List[SyncTypeList])
async def list_(
        page: int = Query(0),
        limit: int = Query(default=10, le=20),
        db: Session = Depends(get_db)
    ):
    """
    list sync types
    """    
    return SyncTypeCrud.list_all(limit, page, db)


@router.post("/", response_model=SyncTypeOut, response_model_exclude=['jobs', 'tasks'])
async def create(sync_type: SyncTypeIn, db: Session = Depends(get_db)):
    """
    create new sync type
    """    
    return SyncTypeCrud.create(sync_type, db)


@router.get("/search/", response_model=List[SyncTypeList], response_model_exclude=sync_type_exclude_list)
async def search(
        name:str = Query(...),
        page: int = Query(0),
        limit: int = Query(default=10, le=20),
        db: Session = Depends(get_db)
    ):
    """
    search sync type by name
    """    
    return SyncTypeCrud.search(name, limit, page, db)


@router.get("/{id}/", response_model=SyncTypeOut)
async def get(id: int, db: Session = Depends(get_db)):
    """
    get sync type
    """    
    return SyncTypeCrud.get(id, db)


@router.put("/{id}/", response_model=SyncTypeOut)
async def update(id: int, payload: SyncTypeIn, db: Session = Depends(get_db)):
    """
    update sync type
    """    
    return SyncTypeCrud.update(id, payload, db)


@router.delete("/{id}/", response_class=ORJSONResponse)
async def delete(id: int, db: Session = Depends(get_db)):
    """
    delete sync type by id
    """
    return SyncTypeCrud.delete(id, db)


@router.get("/all/state/{state}", response_class=ORJSONResponse)
async def change_state_all(state:bool, db: Session = Depends(get_db)):
    """
    enable/disable all synctypes
    """
    return SyncTypeCrud.change_all_state(SyncType.enabled, state, db)


@router.get("/all/notification/{state}", response_class=ORJSONResponse)
async def change_notification_all(state:bool, db: Session = Depends(get_db)):
    """
    enable/disable notification of all synctypes
    """    
    return SyncTypeCrud.change_all_state(SyncType.dispatch_notification, state, db)


@router.get("/{id}/state/{state}", response_model=SyncTypeOut)
async def change_state(id: int, state:bool, db: Session = Depends(get_db)):
    """
    enable/disable synctype
    """    
    return SyncTypeCrud.change_state(id, state, db)


@router.get("/sync/{sync_type}", response_class=ORJSONResponse)
async def sync(
        request: Request,
        sync_type: SyncTypeSet,
        background_tasks: BackgroundTasks,    
        db: Session = Depends(get_db),
        args: Optional[List[str]] = Query([]),
        xargs_keys: Optional[List[str]] = Query([]),
        xargs_vals: Optional[List[str]] = Query([])
    ):
    """
    Sync the given sync type
    """        
    kv = dict(zip(xargs_keys, xargs_vals))
    sync = Sync(sync_type, db, request, *args, **kv)
    background_tasks.add_task(sync.start)

    return ORJSONResponse(
        content=dict(job_id=sync.job_id)
    )

