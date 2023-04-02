from application.initializer import DEFAULT_TOWN
from application.main.components.GenAlg.town import *

def calculate(points):
    new_town = update_town(DEFAULT_TOWN, points)
    new_town_score = calculate_score_for_town(new_town)
    return new_town_score

def get_default():
    return round(calculate_score_for_town(DEFAULT_TOWN),2)