import os

from notifier.db import SessionLocal
from notifier import app
# from notifier.db import Base, engine
from notifier.routers import price_tracker_router, sync_type_router, task_router

from notifier.db import models


# create tables if not found
# Base.metadata.drop_all(bind=engine)
# Base.metadata.create_all(bind=engine)
# Base.metadata.drop_all(bind=engine, tables=[models.Task.__table__])
# Base.metadata.create_all(bind=engine, tables=[models.Task.__table__])

# Base.metadata.drop_all(bind=engine, tables=[models.Job.__table__, models.Task.__table__])
# Base.metadata.create_all(bind=engine, tables=[models.Job.__table__, models.Task.__table__])

# Base.metadata.drop_all(bind=engine, tables=[models.UserTable.__table__])
# Base.metadata.create_all(bind=engine, tables=[models.UserTable.__table__])


API_VER = "v1"

app.include_router(
    sync_type_router,
    prefix=f"/api/{API_VER}/sync-type",
    tags=["SyncType"]
)

if os.environ.get("DEBUG"):
    
    app.include_router(
        price_tracker_router,
        prefix=f"/api/{API_VER}/price_tracker",
        tags=["PriceTracker"]
    )

    app.include_router(
        task_router,
        prefix=f"/api/{API_VER}/task",
        tags=["Tasks"]
    )


    