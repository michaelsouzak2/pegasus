import os
import sys
from datetime import date

import streamlit as st
from streamlit_folium import st_folium

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app.services.copernicus_service import get_bounding_boxes
from app.services.spectator_service import get_acquisition_plan
from app.services.map_generator_service import generate_map

st.set_page_config(page_title="Hércules", layout="wide")

st.title("Projeto Hércules")

st.sidebar.header("Parâmetros de busca")

min_date = date(2025, 10, 1)
default_start = date.today()
default_end = date.today()

start_date = st.sidebar.date_input("Data inicial", value=default_start, min_value=min_date)
end_date = st.sidebar.date_input("Data final", value=default_end, min_value=min_date)

st.markdown("""Use o botão abaixo para consultar o catálogo do Copernicus Dataspace e visualizar os produtos disponíveis na área informada.""")

@st.cache_data
def get_products_cached(start_date, end_date):
    start_date = start_date.isoformat() + "T00:00:00.000Z"
    end_date = end_date.isoformat() + "T23:59:59.000Z"
    
    bounding_boxes = get_bounding_boxes(start_date=start_date, end_date=end_date)
    acquisition_plan = get_acquisition_plan(datetime_of_interest=start_date)

    return (bounding_boxes, acquisition_plan)

    # return get_bounding_boxes(
    #     start_date=start_date.isoformat() + "T00:00:00.000Z",
    #     end_date=end_date.isoformat() + "T23:59:59.000Z"
    # )

@st.cache_data
def generate_map_cached(products):
    return generate_map(products)

products, acquisition_plan = get_products_cached(start_date, end_date)
map = generate_map(products, acquisition_plan)
st_folium(map, use_container_width=True)
