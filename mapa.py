import folium

mapa_sensoriado = folium.Map(location=[-14.2350, -51.9253], zoom_start=4)

mapa_sensoriado.get_root().html.add_child(folium.Element("""
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


mapa_sensoriado.save("mapa_brasil.html")
print("Arquivo gerado: mapa_brasil.html")
