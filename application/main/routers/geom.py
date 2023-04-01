from fastapi.routing import APIRouter
from fastapi import Response, Request, HTTPException, Header, Depends, Query

from pydantic import BaseModel, Field
from typing import List, Union
import json

from application.initializer import logger_instance
from application.main.components.Geom import controller as Geom_controller
from application.main.infrastructure.sql.database import SessionLocal

from sqlalchemy.orm import Session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


router = APIRouter()
logger = logger_instance.get_logger(__name__)


@router.get("/search")
async def geom_search_1(lat: float = 0, lon: float = 0, radius : int = 1500,category : List[str] = Query(None), db: Session = Depends(get_db)):

    response = Geom_controller.search(db, lat, lon, radius, category)

    return response
    