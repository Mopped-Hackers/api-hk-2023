from fastapi.routing import APIRouter
from fastapi import Response, Request, HTTPException, Header, Depends

from pydantic import BaseModel, Field
from typing import List, Union
import json

from application.initializer import logger_instance
from application.main.components.Ai import controller as AI_controller
from application.main.routers.models import AI_input_1, predict_input
from application.main.routers import validation
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


@router.post("/calculate")
async def calculate_1(
    body: AI_input_1,
):
    response = AI_controller.calculate(body)
    return response


@router.get("/default-town")
async def ai_default_1():
    response = AI_controller.get_default()
    return response


@router.post("/predict")
async def ai_predict_1(body: predict_input):
    response = AI_controller.predict(dict(body))
    return response
