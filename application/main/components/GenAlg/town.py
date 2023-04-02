import pandas as pd
import numpy as np

def update_town(town, points):
    new_town = np.copy(town)
    points = dict(points)
    for point in points['points']:
        # print(point[1])
        lat = int(round(float(point.lat) - DEFAULT_MIN_LAT,8) * 1000)
        lon = int(round(float(point.lon) - DEFAULT_MIN_LON,8) * 1000)
        for i in range(max(0, lon - RANGE), min(DEFAULT_MAX_LON-1, lon + RANGE)):
            for j in range(max(0, lat - RANGE), min(DEFAULT_MAX_LAT-1, lat + RANGE)):
                if new_town[j][i] > 15:
                    new_town[j][i] += 0.5
        new_town[lat-1][lon-1] += 1
    print(np.sum(town), np.sum(new_town))
    return new_town

def calculate_score_for_town(town):
    return round(np.sum(town)/BEST_TOWN_SCORE,4) * 100

def compare_towns(town1, town2):
    return town2 - town1

def create_best_town(town):
    print(f"BASE TOWN SCORE - {np.sum(town)}")
    for i in range(town.shape[1]):
        for j in range(town.shape[0]):
            if town[j][i] > 15:
                town[j][i] = 100
    print(f"BEST TOWN SCORE - {np.sum(town)}")
    return np.sum(town)

def create_default_town() -> [[float]]:
    # df = pd.read_csv("kosice_radius_2.csv")
    df = pd.read_csv("./models/kosice_radius_2.csv")
    df['lat'] = df['lat'].astype(float)
    df['lon'] = df['lon'].astype(float)
    df['lat_calc'] = df['lat'] - df['lat'].min()
    df['lon_calc'] = df['lon'] - df['lon'].min()

    df['lon_calc'] = df['lon_calc'].apply(lambda x : round(x,8))
    df['lat_calc'] = df['lat_calc'].apply(lambda x : round(x,8))

    df['lon_calc'] = df['lon_calc'] * 1000
    df['lat_calc'] = df['lat_calc'] * 1000
    
    rows, cols = 91, 52
    arr = np.zeros((cols,rows))

    latMax = int(df['lat_calc'].max())
    lonMax = int(df['lon_calc'].max())
    for index, row in df.iterrows():
        lat = int(row['lat_calc']) - 1
        lon = int(row['lon_calc']) - 1
        for i in range(max(0, lon - RANGE), min(lonMax-1, lon + RANGE)):
            for j in range(max(0, lat - RANGE), min(latMax-1, lat + RANGE)):
                arr[j][i] += 0.5
        arr[lat][lon] = 1
    arr = np.flipud(arr)
    return arr

DEFAULT_MIN_LAT = 48.6936724
DEFAULT_MIN_LON = 21.204655
DEFAULT_MAX_LAT = 52
DEFAULT_MAX_LON = 82
RANGE = 11
BEST_TOWN_SCORE = create_best_town(create_default_town())

    

