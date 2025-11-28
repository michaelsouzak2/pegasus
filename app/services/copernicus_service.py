import os
import sys
import json
import requests
from datetime import date, timedelta
from shapely.geometry import shape
from dotenv import load_dotenv, find_dotenv

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app.config.settings import SETTINGS

_ = load_dotenv(find_dotenv())

"""
Dataset do OpenSARShip: https://opensar.sjtu.edu.cn/DataAndCodes.html
Homepage: https://dataspace.copernicus.eu/
Pesquisa: https://browser.dataspace.copernicus.eu
Primeiros passos: https://documentation.dataspace.copernicus.eu/notebook-samples/sentinelhub/migration_from_scihub_guide.html
Como baixar um produto: https://documentation.dataspace.copernicus.eu/APIs/OData.html#compressed-product-download
Sentinel: https://dataspace.copernicus.eu/data-collections/sentinel-data/sentinel-1

https://api.spectator.earth/?language=Python#spectator-api-docs
https://app.spectator.earth/?&@-21.207458730482642,-35.50781250000001,3z

"""


def get_access_token():
    token_url = "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token"
    payload = {
        "grant_type": "password",
        f"username": {os.getenv("COPERNICUS_USERNAME")},
        "password": {os.getenv("COPERNICUS_PASSWORD")},
        "client_id": "cdse-public"
    }
    resp = requests.post(token_url, data=payload)
    resp.raise_for_status()
    token_info = resp.json()
    access_token = token_info["access_token"]
    return access_token


def get_bounding_boxes(start_date: str = "2025-11-05T00:00:00.000Z", end_date: str = "2025-11-05T23:59:59.000Z") -> list:    
    GEOJSON_PATH = SETTINGS["geojson"]["path_dir"]
    with open(GEOJSON_PATH, "r", encoding="utf-8") as f:
        gj = json.load(f)
    area_of_interest = shape(gj['features'][0]['geometry']).wkt
    data_collection = "SENTINEL-1"
    product_type = "IW_GRDH_1S"

    url = (
        "https://catalogue.dataspace.copernicus.eu/odata/v1/Products?" 
        f"$filter=Collection/Name eq '{data_collection}' and " 
        f"Attributes/OData.CSC.StringAttribute/any(att:att/Name eq 'productType' and att/OData.CSC.StringAttribute/Value eq '{product_type}') and " 
        f"OData.CSC.Intersects(area=geography'SRID=4326;{area_of_interest}') and "
        f"ContentDate/Start ge {start_date} and " 
        f"ContentDate/Start le {end_date}"
        "&$top=1000"
        "&$expand=Attributes"
    )

    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return data["value"]


def download_product(product_id: str, product_name: str, access_token: str, download_path: str):    
    download_url = f"https://download.dataspace.copernicus.eu/odata/v1/Products({product_id})/$value"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get(download_url, headers=headers, stream=True)
    response.raise_for_status()

    filename = os.path.join(download_path, f"{product_name}.zip")
    with open(filename, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    return filename


def start_download_products():
    access_token = get_access_token()
    yesterday = (date.today() - timedelta(1)).isoformat()
    products = get_bounding_boxes(start_date=f"{yesterday}T00:00:00.000Z", end_date=f"{yesterday}T23:59:59.000Z")
    download_path = SETTINGS["download"]["path"]

    for product in products:
        product_id = product["Id"]
        product_name = product["Name"]
        filename = download_product(product_id, product_name, access_token, download_path)
        print(f"Produto {product_name} baixado em {filename}")


if __name__ == "__main__":
    start_download_products()