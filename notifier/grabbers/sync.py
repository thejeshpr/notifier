import os
from uuid import uuid4
from datetime import datetime

from fastapi import Request
from sqlalchemy.orm import Session
import pytz

from notifier.grabbers.base import Base
from notifier.grabbers.tracker import PriceTrackerSync
from notifier.grabbers.bfy import Bfy
from notifier.grabbers.d2 import D2
from notifier.grabbers.rp import RP
from notifier.grabbers.course import DSRCourse
from notifier.grabbers.ng import Ng
from notifier.grabbers.gh_trending import GH
from notifier.grabbers.news import News
from notifier.grabbers.weather import Weather
from notifier.grabbers.yourstry import YS
from notifier.grabbers.hn import HN
from notifier.grabbers.dzone import Dzone
from notifier.grabbers.bkdko import BKdko
from notifier.grabbers.crdko import Crdko
from notifier.grabbers.autocrind import Autocrind
from notifier.grabbers.crwle import Crwle
from notifier.grabbers.twrdsdtsc import Twrdsdtsc
from notifier.grabbers.deepst import DeepSt
from notifier.grabbers.better_advice import BetterAdvice
from notifier.grabbers.in_fit_in_health import InFitInHealth
from notifier.grabbers.psily import PSily
from notifier.grabbers.bpanda import BPanda
from notifier.grabbers.fml import FML
from notifier.grabbers.mm import MM
from notifier.grabbers.avidhya import Avidhya
from notifier.grabbers.gsm import GSM
from notifier.grabbers.frecdcmp import FreCdCmp
from notifier.grabbers.thephoblographer import Thephoblographer
from notifier.grabbers.rdt import Rdt
from notifier.grabbers.better_prog import BetterProg
from notifier.grabbers.mom import MOM
from notifier.grabbers.the_asc import TheAsc

SYNC_GRABBERS = {    
    "pricetracker": PriceTrackerSync.sync,
    "bfy": Bfy.sync,
    "d2": D2.sync,
    "realpython": RP.sync,
    "dsrcourse": DSRCourse.sync,
    "ng": Ng.sync,
    "github_trending": GH.sync,
    "news": News.sync,
    "weather": Weather.sync,
    "ys": YS.sync,
    "hn": HN.sync,
    "dzone": Dzone.sync,
    "bkdko": BKdko.sync,
    "crdko": Crdko.sync,
    "bkdko_road_test": BKdko.bkdko_road_test,
    "crdko_road_test": Crdko.crdko_road_test,
    "autocrind": Autocrind.sync,
    "crwle": Crwle.sync,
    "twrdsdtsc": Twrdsdtsc.sync,
    "deepst": DeepSt.sync,
    "better_advice": BetterAdvice.sync,
    "infit_inhealth": InFitInHealth.sync,
    "psily": PSily.sync,    
    "bpanda": BPanda.sync,
    "fml": FML.sync,
    "mm": MM.sync,
    "avidhya": Avidhya.sync,
    "gsm": GSM.sync,
    "frecdcmp": FreCdCmp.sync,
    "thephoblographer": Thephoblographer.sync,
    "rdt": Rdt.sync,
    "better_programming": BetterProg.sync,
    "mom": MOM.sync,
    "the_asc": TheAsc.sync,
}


class Sync(object):
    def __init__(self, sync_type: str, db: Session, request: Request, *args, **kwargs):        
        self.sync_type = sync_type
        self.job_id = f"{sync_type}:{self.get_current_time()}:{uuid4()}"
        self.obj = Base(sync_type, self.job_id, db, request)
        self.args = args
        self.kwargs = kwargs
        
        
    def start(self):
        """
        execute the sync method
        """
        # check is lock is already acquired
        if not self.obj.sync_type.locked:

            try:
                self.obj.lock()
                # sync only if its enabled
                if self.obj.sync_type.enabled:
                    SYNC_GRABBERS[self.sync_type](self.obj, *self.args, **self.kwargs)
                    self.obj.write_tasks()                    

            except Exception as e:
                self.run(self.obj.job_failed)

            else:
                self.run(self.obj.job_success)
                self.obj.notify()

            finally:
                self.obj.release()

    def run(self, func, *args, **kwargs):
        """
        runs given funciton based sync type enabled or not
        """
        if self.obj.sync_type.enabled:
            func(*args, **kwargs)

    def get_current_time(self):
        fmt = "%H.%M-%D"
        utcmoment_naive = datetime.utcnow()        
        utcmoment = utcmoment_naive.replace(tzinfo=pytz.utc)
        tz = os.environ.get("TZ")
        conv_dt = utcmoment.astimezone(pytz.timezone(tz))
        return conv_dt.strftime(fmt)