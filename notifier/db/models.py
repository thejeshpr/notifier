import os

import datetime
from sqlalchemy import Column, Integer, String, Text, JSON, ForeignKey, Boolean, DateTime
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from notifier.db import Base
import sqlalchemy as sa
from datetime import datetime

from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase

import pytz

def get_current_time():
    utcmoment_naive = datetime.utcnow()
    utcmoment = utcmoment_naive.replace(tzinfo=pytz.utc)
    tz = os.environ.get("TZ")
    return utcmoment.astimezone(pytz.timezone(tz))


class SyncType(Base):
    """
    table for managing the sync types
    """
    __tablename__ = "sync_type"

    created_at              = Column(DateTime, default=get_current_time)
    base_url                = Column(Text, nullable=True)                                      
    dispatch_notification   = Column(Boolean, default=True, nullable=True)
    disable_parse_web       = Column(Boolean, default=True, nullable=True)
    dispatch_to             = Column(String, nullable=True)    
    enabled                 = Column(Boolean, default=True, nullable=True)
    extras                  = Column(JSON, nullable=True)
    id                      = Column(Integer, unique=True, primary_key=True, autoincrement=True)
    jobs                    = relationship('Job', back_populates="sync_type")
    locked                  = Column(Boolean, default=False)    
    name                    = Column(Text, unique=True)
    tasks                   = relationship('Task', back_populates="sync_type")
    time_aware_dispatch     = Column(Boolean, default=False)



class Job(Base):
    """
    table for managing jobs
    """    
    __tablename__ = "jobs"

    created_at      = Column(DateTime(timezone=True), default=get_current_time)  
    err             = Column(Text, nullable=True)
    extras          = Column(JSON, nullable=True)    
    id              = Column(Integer, unique=True, primary_key=True, autoincrement=True)
    status          = Column(String, default="STARTED")
    sync_type       = relationship("SyncType", back_populates="jobs")
    sync_type_id    = Column(Integer, ForeignKey('sync_type.id'))
    tasks           = relationship('Task', back_populates="job")
    unique_key      = Column(String, unique=True, index=True)


class Task(Base):
    """
    table for managing the tasks
    """
    __tablename__ = "tasks"
    
    created_at  = Column(DateTime, default=get_current_time())
    data        = Column(JSON, nullable=True)
    id          = Column(Integer, unique=True, primary_key=True, autoincrement=True)
    job         = relationship("Job", back_populates="tasks")
    job_id      = Column(String, ForeignKey('jobs.id'))
    name          = Column(Text, nullable=True)
    sync_type     = relationship("SyncType", back_populates="tasks")
    sync_type_id  = Column(Integer, ForeignKey('sync_type.id'))
    task_type     = Column(String, nullable=True)
    unique_key    = Column(Text, unique=True, index=True)
    url           = Column(Text, nullable=True)


class PriceTracker(Base):
    """
    table for storeing common info
    """
    __tablename__ = "price_tracker"

    created_at  = Column(sa.DateTime, default=get_current_time)    
    avg_price   = Column(sa.Float, nullable=True)
    curr_price   = Column(sa.Float, nullable=True)
    high_price   = Column(sa.Float, nullable=True)
    low_price   = Column(sa.Float, nullable=True)
    id          = Column(sa.Text, unique=True, primary_key=True)
    title       = Column(sa.Text, index=True, nullable=True)
    image       = Column(sa.Text, nullable=True)
    productUrl = Column(sa.Text, nullable=True)
    store       = Column(sa.Text, nullable=True)
    drop_chance = Column(sa.Integer, nullable=True)
    enabled     = Column(Boolean, default=True, nullable=True)


class UserTable(Base, SQLAlchemyBaseUserTable):
    pass