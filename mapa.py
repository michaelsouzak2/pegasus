import folium
from sentinel_api_client import get_bounding_boxes
from utils import format_date

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
        <b>Origem:</b> {origin}<br>
        <b>Nome:</b> {name}<br>
        <b>Satélite:</b> {satellite}{satellite_identifier}<br>
        <b>Tipo de imagem:</b> {image_type}<br>
        <b>Tipo de produto:</b> {product_type}<br>
        <b>Canais de polização:</b> {polarisation_channels}<br>
        <b>Tamanho:</b> {length}<br>
        <b>Direção da órbita:</b> {direction}<br>
        <b>Início do sensoriamento:</b> {contentdate_start}<br>
        <b>Término do senoriamento:</b> {contentdate_end}<br>
        <b>Data do processamento:</b> {processing_date}<br>
        <b>Data de publicação:</b> {publication_date}<br>
    </div>
    """

    for attr in polygon['Attributes']:
        if attr['Name'] == 'origin':
            origin = attr['Value']
        if attr['Name'] == 'orbitDirection':
            direction = attr['Value']
        if attr['Name'] == 'processingDate':
            processing_date = attr['Value']
        if attr['Name'] == 'productType':
            product_type = attr['Value']
        if attr['Name'] == 'polarisationChannels':
            polarisation_channels = attr['Value']
        if attr['Name'] == 'platformShortName':
            satellite = attr['Value']
        if attr['Name'] == 'platformSerialIdentifier':
            satellite_identifier = attr['Value']
        if attr['Name'] == 'instrumentShortName':
            image_type = attr['Value']

    folium.Polygon(
        locations=[[lat, lon] for lon, lat in polygon['GeoFootprint']['coordinates'][0]],
        color='blue',
        weight=2,
        fill=True,
        fill_color='blue',
        fill_opacity=0.3,
        popup=folium.Popup(html=html_popup.format(
            identify=polygon['Id'],
            origin=origin, 
            name=polygon['Name'], 
            satellite=satellite,
            satellite_identifier=satellite_identifier,
            image_type=image_type,
            product_type=product_type,
            polarisation_channels=polarisation_channels,
            length=f"{polygon['ContentLength'] / (1024 ** 3):.2f} GB",
            direction=direction,
            contentdate_start=format_date(polygon['ContentDate']['Start']),
            contentdate_end=format_date(polygon['ContentDate']['End']), 
            processing_date=format_date(processing_date),
            publication_date=format_date(polygon['PublicationDate'])
        ))
    ).add_to(mapa_copernicus)

mapa_copernicus.save("mapa_brasil.html")
print("Arquivo gerado: mapa_brasil.html")