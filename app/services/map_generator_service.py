import json
import folium
from pathlib import Path

from app.utils.datetime_utils import format_date, get_current_datetime


def create_base_map():
    """
    Cria o mapa base com OSM como padrão e adiciona outras opções de tiles.
    """
    map = folium.Map(
        location=[-14.2350, -51.9253],
        zoom_start=4,
        tiles="OpenStreetMap",
        control_scale=True,
    )

    folium.TileLayer("CartoDB positron", name="CartoDB Claro", show=False).add_to(map)
    folium.TileLayer("CartoDB dark_matter", name="CartoDB Escuro", show=False).add_to(map)
    folium.TileLayer(tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Esri", name="Esri World Imagery", max_zoom=19, show=False,).add_to(map)
    folium.TileLayer(tiles="https://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}", 
        attr="Google", name="Google Maps", max_zoom=20, subdomains=["mt0", "mt1", "mt2", "mt3"], show=False).add_to(map)

    return map


def add_ajb_background(map: folium.Map):
    """
    Adiciona o GeoJSON da AJB marítima
    """
    geojson_path = Path("app/geojson/ajb_simplificado.geojson")
    if not geojson_path.exists():
        return

    with geojson_path.open(encoding="utf-8") as f:
        data = json.load(f)

    geojson_group = folium.FeatureGroup(name="AJB marítima", show=True)

    folium.GeoJson(
        data,
        name="AJB marítima",
        style_function=lambda _: {
            "color": "gray",
            "weight": 1,
            "fillColor": "gray",
            "fillOpacity": 0.2,
        },
    ).add_to(geojson_group)

    geojson_group.add_to(map)


def extract_attr(attrs: list, name: str, default: str = "-") -> str:
    """
    Procura um atributo dentro da lista de Attributes do produto Copernicus.
    """
    for attr in attrs:
        if attr.get("Name") == name:
            return attr.get("Value", default)
    return default


def add_products_polygons(map: folium.Map, products: list):
    """
    Adiciona os polígonos dos produtos retornados pela API ao mapa.
    """
    for product in products:
        attrs = product.get("Attributes", [])

        origin = extract_attr(attrs, "origin")
        direction = extract_attr(attrs, "orbitDirection")
        processing_date = extract_attr(attrs, "processingDate")
        product_type = extract_attr(attrs, "productType")
        polarisation_channels = extract_attr(attrs, "polarisationChannels")
        satellite = extract_attr(attrs, "platformShortName")
        satellite_identifier = extract_attr(attrs, "platformSerialIdentifier")
        image_type = extract_attr(attrs, "instrumentShortName")

        coordinates = product["GeoFootprint"]["coordinates"][0]
        latlon = [[lat, lon] for lon, lat in coordinates]

        popup_html = f"""
        <div style="font-size: 12px;">
            <b>Id:</b> {product.get('Id')}<br>
            <b>Origem:</b> {origin}<br>
            <b>Nome:</b> {product.get('Name')}<br>
            <b>Satélite:</b> {satellite}{satellite_identifier}<br>
            <b>Tipo de imagem:</b> {image_type}<br>
            <b>Tipo de produto:</b> {product_type}<br>
            <b>Canais de polarização:</b> {polarisation_channels}<br>
            <b>Tamanho:</b> {product['ContentLength'] / (1024 ** 3):.2f} GB<br>
            <b>Direção da órbita:</b> {direction}<br>
            <b>Início do sensoriamento:</b> {format_date(product['ContentDate']['Start'])}<br>
            <b>Término do sensoriamento:</b> {format_date(product['ContentDate']['End'])}<br>
            <b>Data de processamento:</b> {format_date(processing_date)}<br>
            <b>Data de publicação:</b> {format_date(product['PublicationDate'])}<br>
        </div>
        """

        folium.Polygon(
            locations=latlon,
            color="blue",
            weight=2,
            fill=True,
            fill_color="blue",
            fill_opacity=0.3,
            popup=folium.Popup(popup_html),
            name=f"Produto {product.get('Id')}",
        ).add_to(map)


def add_fullscreen_style(map: folium.Map):
    """
    Faz com que o mapa ocupe a tela toda.
    """
    map.get_root().html.add_child(
        folium.Element(
            """
            <style>
            html, body { height: 100%; margin: 0; }
            #map { position: absolute; top: 0; bottom: 0; right: 0; left: 0; }
            </style>
            """
        )
    )


def generate_map(products: list):
    """
    Gerador do mapa
    """
    mapa = create_base_map()
    add_ajb_background(mapa)
    add_products_polygons(mapa, products)
    folium.LayerControl(collapsed=False).add_to(mapa)
    add_fullscreen_style(mapa)

    #filename = f"mapa_brasil_{get_current_datetime()}.html"
    #mapa.save(filename)
    #print(f"Arquivo gerado: {filename}")
    return mapa
