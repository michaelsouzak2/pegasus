import os
import json
import requests
from shapely.geometry import shape
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

"""
Dataset do OpenSARShip: https://opensar.sjtu.edu.cn/DataAndCodes.html
Homepage: https://dataspace.copernicus.eu/
Pesquisa: https://browser.dataspace.copernicus.eu
Primeiros passos: https://documentation.dataspace.copernicus.eu/notebook-samples/sentinelhub/migration_from_scihub_guide.html
Como baixar um produto: https://documentation.dataspace.copernicus.eu/APIs/OData.html#compressed-product-download
Sentinel: https://dataspace.copernicus.eu/data-collections/sentinel-data/sentinel-1
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
    with open("app/geojson/ajb_simplificado.geojson", "r", encoding="utf-8") as f:
        gj = json.load(f)
    area_of_interest = shape(gj['features'][0]['geometry']).wkt
    #start_date = "2025-11-05T00:00:00.000Z"
    #end_date = "2025-11-05T23:59:59.000Z"
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


# Download do produto
# --------------------------------
# url = f"https://download.dataspace.copernicus.eu/odata/v1/Products({json['value'][0]['Id']})/$value"

# headers = {"Authorization": f"Bearer {access_token}"}

# session = requests.Session()
# session.headers.update(headers)

# response = session.get(url, stream=True)

# if response.status_code == 200:
#     with open(f"{json['value'][0]['Name']}.zip", "wb") as file:
#         for chunk in response.iter_content(chunk_size=8192):
#             if chunk: 
#                 file.write(chunk)
# else:
#     print(f"Erro ao fazer download. HTTP Status: {response.status_code}")
#     print(response.text)