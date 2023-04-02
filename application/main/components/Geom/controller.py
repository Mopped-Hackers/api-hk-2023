from geoalchemy2 import Geometry
from geoalchemy2.functions import ST_DWithin
from geoalchemy2.elements import WKTElement
from application.main.infrastructure.sql import models
import json
from sqlalchemy.sql import text
from geoalchemy2.types import Geography
from sqlalchemy import or_, and_, distinct, func


def plus(geom_fid, db):
    g = db.query(models.Score).filter(models.Score.geom_id == geom_fid).all()
    if len(g) != 0 :
        db.query(models.Score).filter(models.Score.geom_id == geom_fid).update(
            {"plus": models.Score.plus + 1}
        )
        db.commit()
    else:
        score = models.Score(geom_id=geom_fid, plus=1, minus=0)
        db.add(score)
        db.commit()

def add(point, db):
    new_geom = models.Aminity(
        fid=point.fid,
        aminity=point.aminity,
        lat=point.lat,
        lon=point.lon,
        addressline=point.addressline,
        type=point.type,
        info=point.info,
        build=0,
        geom=f"POINT({point.lon} {point.lat})",
    )

    db.add(new_geom)
    db.commit()
    plus(point.fid, db)



def score(geom_fid, db):
    return db.query(models.Score).filter(models.Score.geom_id == geom_fid).first()

def minus(geom_fid, db):
    g = db.query(models.Score).filter(models.Score.geom_id == geom_fid).all()
    if len(g) != 0 :
        db.query(models.Score).filter(models.Score.geom_id == geom_fid).update(
            {"plus": models.Score.minus + 1}
        )
        db.commit()
    else:
        score = models.Score(geom_id=geom_fid, plus=0, minus=1)

        db.add(score)
        db.commit()

def search_build(db, category):
    if category == None or category == "all":
        category = get_categories(db)

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
                models.Aminity.build,
            )
            .filter(
                and_(
                    models.Aminity.aminity.in_(category)),
                    models.Aminity.build == 1
                )
            .all()
        )

    points = [transform_point_for_fe(r) for r in result]
    return points

def search_all(db, category, vote):
    if category == None or category == "all":
        category = get_categories(db)

    if vote:
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
                models.Aminity.build,
            )
            .filter(
                and_(models.Aminity.aminity.in_(category), models.Aminity.build == 0)
            )
            .all()
        )
    else:
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
                models.Aminity.build,
            )
            .filter(models.Aminity.aminity.in_(category))
            .all()
        )

    points = [transform_point_for_fe(r) for r in result]
    return points


def get_color_by_aminity(aminity):
    c2a = {
        "Culture": "red",
        "Drug store": "white",
        "Green place": "green",
        "Hospital": "yellow",
        "Job": "purple",
        "School": "blue",
        "Shop": "orange",
        "Sport": "pink",
        "Transport": "black",
    }
    return c2a.get(aminity, "black")


def transform_point_for_fe(x):
    r = x
    new = {
        "type": "Feature",
        "properties": {
            "fid": r[0],
            "aminity": r[1],
            "lat": r[2],
            "lon": r[3],
            "name": r[4],
            "type": r[5],
            "addressline": r[6],
            "info": r[7],
            "build": r[8],
            "color": get_color_by_aminity(r[1]),
        },
        "geometry": {"type": "Point", "coordinates": [r[3], r[2]]},
    }
    return new


def find_missing(result, category):
    response = {"points": [], "build": [], "missing": []}
    for r in result:
        r = transform_point_for_fe(r)
        response["points"].append(r)

        if not r["properties"]["aminity"] in response["build"]:
            response["build"].append(r["properties"]["aminity"])

    for c in category:
        if c not in response["build"]:
            response["missing"].append(c)
    return response


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
            models.Aminity.build,
        )
        .filter(
            and_(
                ST_DWithin(
                    models.Aminity.geom.cast(Geography),
                    WKTElement(center_point, srid=4326),
                    radius,
                ),
                models.Aminity.aminity.in_(category),
            )
        )
        .all()
    )

    # points = [transform_point_for_fe(r) for r in result]
    points = find_missing(result, get_categories(db))

    return points


def get_categories(db):
    result = db.query(models.Aminity.aminity).distinct(models.Aminity.aminity).all()
    result = [r[0] for r in result]
    return result


def count_by_category(db):
    result = (
        db.query()
        .with_entities(models.Aminity.aminity, func.count(models.Aminity.id))
        .group_by(models.Aminity.aminity)
        .all()
    )
    output = []
    for r in result:
        output.append({r[0]: r[1]})
    return output
