import folium
from sentinel_api_client import get_bounding_boxes

images = get_bounding_boxes()

polygons = [coordinates['GeoFootprint']['coordinates'][0] for coordinates in images]

mapa_copernicus = folium.Map(location=[-14.2350, -51.9253], zoom_start=4)

mapa_copernicus.get_root().html.add_child(folium.Element("""
<style>
html, body {
    height: 100%;
    margin: 0;
}
#map {
    position: absolute;
    top: 0;
    bottom: 0;
    right: 0;
    left: 0;
}
</style>
"""))

for polygon in polygons:
    folium.Polygon(
        locations=[[lat, lon] for lon, lat in polygon],
        color='blue',
        weight=2,
        fill=True,
        fill_color='blue',
        fill_opacity=0.5
    ).add_to(mapa_copernicus)

mapa_copernicus.save("mapa_brasil.html")
print("Arquivo gerado: mapa_brasil.html")
