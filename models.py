from sqlalchemy import CheckConstraint, Column, Float, Integer, String, Table, Text, text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql.sqltypes import NullType

Base = declarative_base()
metadata = Base.metadata


class Aminity(Base):
    __tablename__ = 'aminity'

    id = Column(Integer, primary_key=True, server_default=text("nextval('aminity_id_seq'::regclass)"))
    fid = Column(Text)
    aminity = Column(Text)
    lat = Column(Float(53))
    lon = Column(Float(53))
    name = Column(Text)
    addressline = Column(Text)
    type = Column(Text)
    info = Column(JSONB)
    geom = Column(NullType)

