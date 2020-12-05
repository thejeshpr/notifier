from calendar import monthrange
from datetime import datetime, timedelta, date

from fastapi import Request
from sqlalchemy import func, and_
from sqlalchemy.orm import Session

from notifier.db import models 


DATE_FORMAT = "%Y-%m-%d"


class SyncTypeHelper(object):

    @staticmethod
    def get_all_sync_types_with_stats(db: Session, request: Request):
        """
        fetch all sync types along with jobs & tasks
        """
        job_sq = JobHelper.sq_count_by_sync_type(db)
        task_sq = TaskHelper.sq_count_by_sync_type(db)

        sync_types = db.query(
                        models.SyncType,
                        job_sq.c.count,
                        task_sq.c.count
                    ).join( 
                        (job_sq, job_sq.c.sync_type_id == models.SyncType.id),
                        (task_sq, task_sq.c.sync_type_id == models.SyncType.id)
                    ).order_by(models.SyncType.id.asc())\
                    .all() 

        context = dict(
            items=sync_types,
            request=request
        )
        
        return dict(
            name="sync_types.html",
            context=context
        )
        
    @staticmethod
    def dashboard(
            db:Session,
            request: Request,
            day: int,
            month: int,
            year: int,
            delta: int
        ):
        """
        returns dashboard content
        """

        # if day and month and year:
        #     from_date = datetime(year, month, day)
        # else:
        #     from_date = datetime(datetime.today().year, datetime.today().month, datetime.today().day)

        try:
            from_date = datetime(year, month, day)
        except Exception as e:
            from_date = datetime(datetime.today().year, datetime.today().month, datetime.today().day)

        ref_dat = from_date

        if delta:            
            from_date = from_date + timedelta(days=delta)

        to_date = from_date + timedelta(days=1)   

        task_sq = TaskHelper.sq_count_by_sync_type_and_date(db, from_date, to_date)
        job_sq = JobHelper.sq_count_by_sync_type_and_date(db, from_date, to_date)

        res = db.query(
                    models.SyncType,
                    task_sq.c.count,
                    job_sq.c.count
                )\
                .outerjoin(
                    (job_sq, job_sq.c.sync_type_id == models.SyncType.id),
                    (task_sq, task_sq.c.sync_type_id == models.SyncType.id)
                )\
                .order_by(task_sq.c.count.desc())\
                .all()

        # sort items by count
        sorted_items = sorted(res, key=lambda x:x[1] if x[1] else 0, reverse=True)
        
        # calculate task count
        count = 0
        for r in res:
            if r[1]:
                count = count + int(r[1])

        context = dict(
            items   = sorted_items,
            from_dt = f"{from_date.day}/{from_date.month}/{from_date.year}",
            to_dt   = f"{to_date.day}/{to_date.month}/{to_date.year}",
            days    = range(1, monthrange(from_date.year, from_date.month)[1] + 1),
            months  = range(1, 13),
            years   = range(2020, 2022),
            request = request,
            delta   = delta,

            from_date   = from_date.strftime(DATE_FORMAT),
            to_date     = to_date.strftime(DATE_FORMAT),
            task_count  = count,

            selected_day    = ref_dat.day,
            selected_month  = ref_dat.month,
            selected_year   = ref_dat.year,
            current_page    = "Dashboard",
        )
            
        return dict(
            name="dashboard.html",
            context=context
        )


class TaskHelper(object):

    @staticmethod
    def sq_count_by_sync_type(db: Session):
        """
        returns sub query of tasks count group by sync types
        """
        return db.query(
                models.Task.sync_type_id,
                func.count(models.Task.sync_type_id).label('count')
            )\
            .group_by(models.Task.sync_type_id)\
            .subquery()

    @staticmethod
    def sq_count_by_sync_type_and_date(
            db: Session,
            from_date,
            to_date
        ):
        """
        returns sub query of tasks count group by sync types and between dates
        """
        # from_date = datetime(2020, 11, 1)
        # to_date = datetime(2020, 11, 30)
        # print(dir(func))
        # print(db.query(
        #             models.Task.sync_type_id,
        #             func.count(models.Task.sync_type_id).label('count'),
        #             func.strftime("%Y-%m-%d", models.Task.created_at)
        #         )\
        #         .filter(
        #             and_(
        #                 models.Task.created_at >= from_date,
        #                 models.Task.created_at <= to_date,
        #             )
        #         )\
        #         .group_by(models.Task.sync_type_id, func.strftime("%Y-%m-%d", models.Task.created_at))\
        #         .all())
        return db.query(
                    models.Task.sync_type_id,
                    func.count(models.Task.sync_type_id).label('count')
                )\
                .filter(
                    and_(
                        models.Task.created_at >= from_date,
                        models.Task.created_at <= to_date,
                    )
                )\
                .group_by(models.Task.sync_type_id)\
                .subquery()
    


class JobHelper(object):
    """
    Helper for Job related views
    """

    @staticmethod
    def sq_count_by_sync_type(db: Session):
        """
        returns sub query of jobs count group by sync types
        """
        return db.query(
                    models.Job.sync_type_id,
                    func.count(models.Job.sync_type_id).label('count')
                )\
                .group_by(models.Job.sync_type_id)\
                .subquery()

    @staticmethod
    def sq_count_by_sync_type_and_date(
            db: Session,
            from_date,
            to_date
        ):
        """
        returns sub query of jobs count group by sync types and between dates
        """
        return db.query(
                    models.Job.sync_type_id,
                    func.count(models.Job.sync_type_id).label('count')
                )\
                .filter(
                    and_(
                        models.Job.created_at >= from_date,
                        models.Job.created_at <= to_date,
                    )
                )\
                .group_by(models.Job.sync_type_id)\
                .subquery()