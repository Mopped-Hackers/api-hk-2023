from application.initializer import DEFAULT_TOWN
from application.main.components.GenAlg.town import *
from application.main.components.GenAlg.algo import *
from application.main.components.Geom.controller import *


def calculate(points):
    new_town = update_town(DEFAULT_TOWN, points)
    new_town_score = calculate_score_for_town(new_town)
    return new_town_score

def calculate_2(points):
    new_town = update_town_2(DEFAULT_TOWN, points)
    new_town_score = calculate_score_for_town(new_town)
    return new_town_score


def get_default():
    return round(calculate_score_for_town(DEFAULT_TOWN), 2)


def transform_mid_points(points):
    lat = points[0] / 1000 + DEFAULT_MIN_LAT
    lon = points[1] / 1000 + DEFAULT_MIN_LON
    return lat, lon


def predict(body):
    radius = body["radius"]
    toSelect = []
    numFacilities = []
    list_of_aminities = []
    for aminity in body["aminity"]:
        name = aminity.name
        toSelect.append(name)
        count = aminity.count
        numFacilities.append(count)
        for c in range(count):
            list_of_aminities.append(name)
    arr, midPoints = request_func(toSelect, numFacilities, radius)
    points = []

    predicted_aminities = []
    ind = 0
    for i, j in enumerate(midPoints):
        for midpoint in midPoints[i]:
            lat, lon = transform_mid_points(midpoint)

            points.append({
                "lat" : lat,
                "lon" : lon
            })

            predicted_aminities.append(
                {
                    "type": "Feature",
                    "properties": {
                        "fid": "KULO",
                        "aminity": list_of_aminities[ind],
                        "lat": lat,
                        "lon": lon,
                        "name": "Predicted",
                        "type": "Predicted",
                        "addressline": "Xxxxx",
                        "info": "",
                        "build": 0,
                        "color": get_color_by_aminity(list_of_aminities[ind]),
                    },
                    "geometry": {"type": "Point", "coordinates": [lon, lat]},
                }
            )
            ind += 1

    new_score = calculate_2({
        "points" : points
    })

    return {
        "points" : predicted_aminities,
        "score" : round(new_score,4)
    }
