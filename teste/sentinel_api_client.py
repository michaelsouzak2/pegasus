import requests
import json
from shapely.geometry import shape
import pandas as pd
import os
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

start_date = "2025-11-05"
end_date = "2025-11-05"
data_collection = "SENTINEL-1"

with open("ajb_simplificado.geojson", "r", encoding="utf-8") as f:
    gj = json.load(f)
aoi = shape(gj['features'][0]['geometry']).wkt

start_date = "2025-11-05T00:00:00.000Z"
end_date = "2025-11-05T23:59:00.000Z"
data_collection = "SENTINEL-1"

url = f"https://catalogue.dataspace.copernicus.eu/odata/v1/Products?$filter=Collection/Name eq '{data_collection}' and OData.CSC.Intersects(area=geography'SRID=4326;{aoi}') and ContentDate/Start gt {start_date} and ContentDate/Start lt {end_date}"

json = requests.get(url).json()
print(pd.DataFrame.from_dict(json["value"]).head(5))


# Download do produto
#--------------------------------
url = f"https://download.dataspace.copernicus.eu/odata/v1/Products({json['value'][0]['Id']})/$value"

headers = {"Authorization": f"Bearer {access_token}"}

session = requests.Session()
session.headers.update(headers)

response = session.get(url, stream=True)

if response.status_code == 200:
    with open("produto.zip", "wb") as file:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk: 
                file.write(chunk)
else:
    print(f"Erro ao fazer download. HTTP Status: {response.status_code}")
    print(response.text)