from geoalchemy2 import Geometry
from geoalchemy2.functions import ST_DWithin
from geoalchemy2.elements import WKTElement
from application.main.infrastructure.sql import models
import json
from sqlalchemy.sql import text
from geoalchemy2.types import Geography
from sqlalchemy import or_, and_,distinct


def transform_point_for_fe(x):
    r = dict(x)
    new = {
        "type": "Feature",
        "properties": r,
        "geometry": {"type": "Point", "coordinates": [r["lon"], r["lat"]]},
    }
    return new

def add(point, db):
    new_geom = models.Aminity(
                    fid = point.fid,
                    aminity = point.aminity,
                    lat = point.lat,
                    lon = point.lon,
                    addressline = point.addressline,
                    type = point.type,
                    info = point.info,
                    geom = f'POINT({point.lon} {point.lat})'

                    )

    db.add(new_geom)   
    db.commit()

def search_all(db, category):
    if category == None or category == "all":
        category = get_categories(db)
    print(category)
    result = (
        db.query(
            models.Aminity.fid,
            models.Aminity.aminity,
            models.Aminity.lat,
            models.Aminity.lon,
            models.Aminity.name,
            models.Aminity.type,
            models.Aminity.addressline,
            models.Aminity.info,
        )
        .filter(
            models.Aminity.aminity.in_(category)    
        ).all()
    )
    

    points = [transform_point_for_fe(r) for r in result]

    return points

def search(db, lat, lon, radius, category):
    if category == None or category == "all":
        category = get_categories(db)
    center_point = "POINT({lon} {lat})".format(lat=lat, lon=lon)
    result = (
        db.query(
            models.Aminity.fid,
            models.Aminity.aminity,
            models.Aminity.lat,
            models.Aminity.lon,
            models.Aminity.name,
            models.Aminity.type,
            models.Aminity.addressline,
            models.Aminity.info,
        )
        .filter(
            and_(
                ST_DWithin(
                models.Aminity.geom.cast(Geography),
                WKTElement(center_point, srid=4326),
                radius,
            ), 
            models.Aminity.aminity.in_(category)
            )
            
        )
        .all()
    )

    points = [transform_point_for_fe(r) for r in result]

    return points

def get_categories(db):

    result = db.query(models.Aminity.aminity).distinct(models.Aminity.aminity).all()
    result = [r['aminity'] for r in result]
    return result