import os
import sys
import json

import requests
import geopandas as gpd
from shapely.geometry import shape

from dotenv import load_dotenv, find_dotenv

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app.config.settings import SETTINGS

_ = load_dotenv(find_dotenv())

SPECTATOR_URL = SETTINGS["urls"]["spectator_url"]

def get_acquisition_plan(datetime_of_interest: str) -> dict:
    """
    Consulta o plano de aquisição do Spectator Earth para a área de interesse e intervalo de datas fornecidos.
    """

    area_of_interest = gpd.read_file(SETTINGS["geojson"]["path_dir"])
    aoi_geom = area_of_interest.union_all() # Retorna a geometria unificada da área de interesse
    
    satellites = "Sentinel-1A,Sentinel-1C"
    # datetime_of_interest = "2025-11-15T00:00:00Z"
    url = f"{SPECTATOR_URL}?satellites={satellites}&datetime={datetime_of_interest}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        acquisition_plan = response.json()

        intersecting_features = []

        for feature in acquisition_plan.get("features", []):
            geometry = feature.get("geometry")
            if geometry:
                geom_shape = shape(geometry)
                # inside =  area_of_interest.intersects(geom_shape)
                if geom_shape.intersects(aoi_geom):
                    intersecting_features.append(feature)

        return {
            "type": "FeatureCollection",
            "features": intersecting_features
        }
    except requests.RequestException as e:
        print(f"Erro ao consultar o Spectator Earth: {e}")
        return None
    
# get_acquisition_plan("2025-11-15T00:00:00Z")


    


