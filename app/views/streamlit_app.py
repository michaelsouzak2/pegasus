from datetime import date, datetime, time

import folium
import streamlit as st
from streamlit_folium import st_folium

from app.services.copernicus_service import get_bounding_boxes
from app.services.map_generator_service import generate_map

st.set_page_config(page_title="Hércules", layout="wide")

st.title("Consulta de Produtos Copernicus")

st.sidebar.header("Parâmetros de busca")

min_date = date(2020, 1, 1)
default_start = date.today()
default_end = date.today()

start_date = st.sidebar.date_input("Data inicial", value=default_start, min_value=min_date)
end_date = st.sidebar.date_input("Data final", value=default_end, min_value=min_date)

st.markdown("""Use o botão abaixo para consultar o catálogo do Copernicus Dataspace e visualizar os produtos disponíveis na área informada.""")

map = folium.Map(
        location=[-14.2350, -51.9253],
        zoom_start=4,
        tiles="OpenStreetMap",
        control_scale=True,
    )


st_data = st_folium(map)
