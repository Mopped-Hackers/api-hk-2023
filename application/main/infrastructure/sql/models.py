from sqlalchemy.orm import declarative_base, relationship
from .database import Base, metadata

from sqlalchemy import Column, Integer, String, Float, JSON, text
from sqlalchemy.dialects.postgresql import JSONB, TEXT
from sqlalchemy.ext.declarative import declarative_base
from geoalchemy2 import Geometry
Base = declarative_base()

class Aminity(Base):
    __tablename__ = 'aminity'
    id = Column(Integer, primary_key=True)
    fid = Column(TEXT)
    aminity = Column(TEXT)
    lat = Column(Float)
    lon = Column(Float)
    name = Column(TEXT)
    addressline = Column(TEXT)
    type = Column(TEXT)
    info = Column(JSONB)
    build = Column(Integer)
    geom = Column(Geometry('POINT'))

class Score(Base):
    __tablename__ = 'score'
    id = Column(Integer, primary_key=True)
    geom_id  = Column(TEXT)
    plus = Column(Integer)
    minus = Column(Integer)