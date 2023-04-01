from geoalchemy2 import Geometry
from geoalchemy2.functions import ST_DWithin
from geoalchemy2.elements import WKTElement
from application.main.infrastructure.sql import models
import json
from sqlalchemy.sql import text
from geoalchemy2.types import Geography
from sqlalchemy import or_, and_

def transform_point_for_fe(x):
    r = dict(x)
    new = {
        "type": "Feature",
        "properties": r,
        "geometry": {"type": "Point", "coordinates": [r["lon"], r["lat"]]},
    }
    return new


def search(db, lat, lon, radius, category):
    if category == None or category == "all":
        category = [
            "GreenPlace",
            "Job",
            "Shop",
            "Sport",
            "Drug store",
            "culture",
            "Transport",
            "School",
            "Hospital",
        ]
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
