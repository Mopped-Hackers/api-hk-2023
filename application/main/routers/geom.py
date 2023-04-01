from fastapi.routing import APIRouter
from fastapi import Response, Request, HTTPException, Header, Depends, Query
from pydantic import BaseModel, Field
from typing import List, Union
import json
from application.initializer import logger_instance
from application.main.components.Geom import controller as Geom_controller
from application.main.infrastructure.sql.database import SessionLocal
from application.main.routers.models import DefaultGeom
from sqlalchemy.orm import Session

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


router = APIRouter()
logger = logger_instance.get_logger(__name__)


@router.get("/score/plus/{geom_fid}")
async def geom_score_plus(
    geom_fid: str,db: Session = Depends(get_db)
):
     response = Geom_controller.plus(geom_fid, db)
     return response

@router.get("/score/minus/{geom_fid}")
async def geom_score_minus(
    geom_fid: str,db: Session = Depends(get_db)
):
     response = Geom_controller.minus(geom_fid, db)
     return response

@router.get("/score/{geom_fid}")
async def geom_score(
    geom_fid: str,db: Session = Depends(get_db)
):
     response = Geom_controller.score(geom_fid, db)
     return response

@router.post("/add")
async def geom_add(point : DefaultGeom = None,db: Session = Depends(get_db)):
    response = Geom_controller.add(point, db)
    return 200

@router.get("/all")
async def geom_search_2(category : List[str] = Query(None),db: Session = Depends(get_db)):
    response = Geom_controller.search_all(db, category)
    return response

@router.get("/search")
async def geom_search_1(lat: float = 0, lon: float = 0, radius : int = 1500,category : List[str] = Query(None), db: Session = Depends(get_db)):
    response = Geom_controller.search(db, lat, lon, radius, category)
    return response
    
@router.get("/categories")
async def geom_categories(db: Session = Depends(get_db)):
    response = Geom_controller.get_categories(db)
    return response
    