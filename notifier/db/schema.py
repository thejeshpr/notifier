from datetime import date, datetime, time, timedelta
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, HttpUrl, Field, Json, validator, ValidationError
from enum import Enum


class TaskType(str, Enum):
    message = "message"
    video = "video"
    photo = "photo"


class TaskIn(BaseModel):
    unique_key: str
    data: Optional[Dict[str, Any]] = {}
    name: str
    task_type: TaskType
    url: Optional[str] = None

    class Config:
        orm_mode = True


class Job(BaseModel):
    unique_key: str
    sync_type: str
    status: str

class JobOut(BaseModel):
    id: int
    unique_key: str
    status: Optional[str]
    err: Optional[str]
    extras: Optional[Dict[str, Any]] = {}
    created_at: Optional[datetime] = None
    # sync_type: SyncTypeOut
    tasks: Optional[List[TaskIn]]

    # its possible to give foreign key ref like below
    # sync_type = SyncTypeOut
    class Config:
        orm_mode = True


# date format
# 2020-10-16T16:59:58.748183+00:00
# YYYY-MM-DD[T]HH:MM[:SS[.ffffff]][Z[±]HH[:]MM]]]

class SyncTypeIn(BaseModel):
    base_url: Optional[HttpUrl] = None
    # dispatch_key: Optional[str] = None
    # dispatch_type: Optional[str]
    dispatch_notification: Optional[bool] = False
    disable_parse_web: Optional[bool] = True
    dispatch_to: Optional[str]    
    enabled: Optional[bool] = True
    extras: Optional[Dict[str, Any]] = {}
    locked: Optional[bool] = False
    name: str
    time_aware_dispatch: Optional[bool] = False
    

    class Config:
        orm_mode = True


    # it validated the while returning the data also
    # @validator('name')
    # def unique_name(cls, v):                
    #     db = SessionLocal()
    #     count = db.query(models.SyncType).filter(models.SyncType.name == v).count()        
    #     db.close()
    #     if count:
    #         raise ValueError(f"SyncType already exist with name '{v}'")
        
    #     return v



class SyncTypeOut(SyncTypeIn):
    id: int
    created_at: Optional[datetime]
    # jobs: Optional[List[JobOut]]
    # tasks: Optional[List[TaskIn]]    


class SyncTypeList(BaseModel):
    id: int
    base_url: Optional[str] = None
    name: str
    enabled: bool
    dispatch_to: str
    dispatch_notification: bool
    created_at: Optional[datetime]
    extras: Optional[Dict[str, Any]] = {}

    class Config:
        orm_mode = True


class ProductInfo(BaseModel):
    avg_price: Optional[float]
    curr_price: float
    drop_chance: Optional[int]
    high_price: Optional[float]
    low_price: Optional[float]
    id: str
    store: str
    title: str
    image: Optional[HttpUrl]    
    productUrl: HttpUrl
    enabled: Optional[bool] = True

    class Config:
        orm_mode = True


class PriceTrackerIn(BaseModel):
    url: HttpUrl

