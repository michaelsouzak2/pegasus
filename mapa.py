import folium
from sentinel_api_client import get_bounding_boxes

images = get_bounding_boxes()

# polygons = [coordinates['GeoFootprint']['coordinates'][0] for coordinates in images]

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

for polygon in images:

    html_popup = """
    <div>
        <b>Id:</b> {identify}<br>
        <b>Nome:</b> {name}<br>
        <b>Tamanho:</b> {length}<br>
        <b>Publicado em:</b> {publication_date}<br>
        <b>Início da passagem:</b> {contentdate_start}<br>
        <b>Término da passagem:</b> {contentdate_end}<br>
    </div>
    """

    folium.Polygon(
        locations=[[lat, lon] for lon, lat in polygon['GeoFootprint']['coordinates'][0]],
        color='blue',
        weight=2,
        fill=True,
        fill_color='blue',
        fill_opacity=0.3,
        popup=folium.Popup(html=html_popup.format(
            identify=polygon['Id'], 
            name=polygon['Name'], 
            length=f"{polygon['ContentLength'] / (1024 ** 3):.2f} GB",
            publication_date=polygon['PublicationDate'],
            contentdate_start=polygon['ContentDate']['Start'],
            contentdate_end=polygon['ContentDate']['End'])
        )
    ).add_to(mapa_copernicus)

mapa_copernicus.save("mapa_brasil.html")
print("Arquivo gerado: mapa_brasil.html")