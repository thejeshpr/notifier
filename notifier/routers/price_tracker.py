from typing import List, Optional
from fastapi import APIRouter, Query, Depends
from fastapi.responses import ORJSONResponse, JSONResponse
from sqlalchemy.orm import Session

from notifier.db.schema import PriceTrackerIn, ProductInfo
from notifier.db.models import PriceTracker
from notifier.grabbers import Tracker
from notifier.views import get_db


class PriceTrackerCRUD(object):
    """
    class for pricetracker crud operations
    """
    @classmethod
    def create(cls, payload: PriceTrackerIn, db: Session) -> ProductInfo:
        """
        create new price tracker
        """
        product = Tracker.get_poduct_info(payload.url)    

        # check if url already exist
        if db.query(PriceTracker).filter(PriceTracker.productUrl == product.productUrl).count():
            return ORJSONResponse(
                status_code=403,
                content={"error": f"Tracker already exist with URL"}
            )    
        
        obj = PriceTracker(**product.dict())
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return product
    
    @classmethod
    def search(cls, q: str, limit: int, page: int, db: Session) -> List[PriceTracker]:
        """
        search for product by name
        """
        return db.query(PriceTracker)\
                .filter(PriceTracker.title.contains(f"{q}%"))\
                .limit(limit).offset(page * limit)\
                .all()

    @classmethod
    def list_all(cls, limit: int, page: int, db: Session) -> List[PriceTracker]:
        """
        list all pricetraker
        """
        return db.query(PriceTracker).limit(limit).offset(page * limit).all()

    @classmethod
    def get(cls, id: str, db: Session) -> PriceTracker:
        """
        returns pricetracker by id
        """
        obj = db.query(PriceTracker).filter(PriceTracker.id == id).first()
        if obj:
            return obj
        else:
            return PriceTrackerCRUD.response_404(id)

    @classmethod
    def delete(cls, id: str, db: Session) -> ORJSONResponse:
        """
        delete pricetracker by id
        """
        count = db.query(PriceTracker).filter(PriceTracker.id == id).delete()        
        db.commit()
        if not count:
            return PriceTrackerCRUD.response_404(id)
        else:
            return PriceTrackerCRUD.response_200(f"Deleted Item with id {id}")

    @classmethod
    def change_state(cls, id: str, state: bool, db: Session) -> PriceTracker:
        """
        update tracker enabled state and return item
        """
        obj = db.query(PriceTracker).filter(PriceTracker.id == id).first()        
        if obj:
            obj.enabled = state
            db.commit()
            return obj
        else:
            return PriceTrackerCRUD.response_404(id)

    @classmethod
    def response_404(cls, id: str) -> JSONResponse:
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
    def response_200(cls, info: str) -> JSONResponse:
        """
        return JSON response
        """
        return ORJSONResponse( content=dict( ok=True,info=info ) )



router = APIRouter()

@router.get("/", response_model=List[ProductInfo])
async def list_(page: int = Query(0), limit: int = Query(default=10, le=20), db: Session = Depends(get_db)):
    """
    list trackers
    """
    return PriceTrackerCRUD.list_all(limit, page, db)


@router.post("/", response_model=ProductInfo)
async def create(payload: PriceTrackerIn, db: Session = Depends(get_db)):
    """
    create new tracker
    """    
    return PriceTrackerCRUD.create(payload, db)


@router.get("/search/", response_model=List[ProductInfo])
async def search(
        q:str = Query(...),
        page: int = Query(0),
        limit: int = Query(default=10, le=20),
        db: Session = Depends(get_db)
    ):
    """
    search trackers
    """  
    return PriceTrackerCRUD.search(q, limit, page, db)
    

@router.get("/{id}/", response_model=ProductInfo)
async def get(id: str, db: Session = Depends(get_db)):
    """
    get space
    """    
    return PriceTrackerCRUD.get(id, db)


@router.delete("/{id}/", response_class=ORJSONResponse)
async def delete(id: str, db: Session = Depends(get_db)):
    """
    delete tracker
    """    
    return PriceTrackerCRUD.delete(id, db)    


@router.get("/{id}/state/{state}", response_model=ProductInfo)
async def enable(id: str, state:bool, db: Session = Depends(get_db)):
    """
    enable/disable trackers
    """    
    return PriceTrackerCRUD.change_state(id, state, db)
