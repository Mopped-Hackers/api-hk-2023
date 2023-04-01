from geoalchemy2 import Geometry
from geoalchemy2.functions import ST_DWithin
from geoalchemy2.elements import WKTElement
from application.main.infrastructure.sql import models
import json
from sqlalchemy.sql import text
from geoalchemy2.types import Geography
from sqlalchemy import or_, and_,distinct,func


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

def score(geom_fid, db):
    return db.query(models.Score).filter(models.Score.geom_id == geom_fid).first()

def plus(geom_fid, db):
    g = db.query(models.Score).filter(models.Score.geom_id == geom_fid).all()
    if g:
        db.query(models.Score).filter(models.Score.geom_id == geom_fid).update({'plus': models.Score.plus + 1})
        db.commit()
    else:
        score = models.Score(
                    geom_id = geom_fid,
                    plus = 1,
                    minus = 0
                    )

        db.add(score)   
        db.commit()

def minus(geom_fid, db):
    g = db.query(models.Score).filter(models.Score.geom_id == geom_fid).all()
    if g:
        db.query(models.Score).filter(models.Score.geom_id == geom_fid).update({'plus': models.Score.minus + 1})
        db.commit()
    else:
        score = models.Score(
                    geom_id = geom_fid,
                    plus = 0,
                    minus = 1
                    )

        db.add(score)   
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


def transform_point_for_fe(x):
    r = dict(x)
    new = {
        "type": "Feature",
        "properties": r,
        "geometry": {"type": "Point", "coordinates": [r["lon"], r["lat"]]},
    }
    return new

def find_missing(result,category):
    response = {
        "points" : [],
        "build" : [],
        "missing"  :[]
    }
    for r in result:
        r = transform_point_for_fe(r)
        
        response['points'].append(r)
        
        if not r['properties']['aminity'] in response['build']:
            response['build'].append(r['properties']['aminity'])
        
    for c in category:
        if c not in response['build']:
            response['missing'].append(c)
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

    # points = [transform_point_for_fe(r) for r in result]
    points = find_missing(result,get_categories(db))

    return points

def get_categories(db):

    result = db.query(models.Aminity.aminity).distinct(models.Aminity.aminity).all()
    result = [r['aminity'] for r in result]
    return result

def count_by_category(db):

    result = (
        db.query(models.Aminity.aminity, func.count()).group_by(models.Aminity.aminity).all()
    )
    return result