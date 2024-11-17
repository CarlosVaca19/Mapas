import folium
import pandas as pd

# Leer los datos de los volcanes, obteniendo listas de latitudes, longitudes, elevaciones y nombres.
data = pd.read_csv("App - Mapas/Volcanoes.txt")
latitudes = list(data["LAT"])
longitudes = list(data["LON"])
elevations = list(data["ELEV"])  # Elevaciones para mostrar en el marcador
names = list(data["NAME"])

# Función para determinar el color del marcador según la elevación del volcán.
def color_volcan(elevation):
    if elevation < 1000:
        return 'green'
    elif 1000 <= elevation < 3000:
        return 'orange'
    else:
        return 'red'

# HTML para el popup, con enlace a Google para buscar información sobre el volcán.
html_template = """
Nombre del volcán:<br>
<a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
Altura: %s m
"""

# Crear el mapa con una ubicación inicial y un nivel de zoom especificado.
mapa = folium.Map(location=[38.58, -99.09], zoom_start=5, titles="Stamen Terrain")

# Crear un grupo de características para los marcadores de volcanes.
fg_volcanes = folium.FeatureGroup(name="Volcanes")

# Añadir un marcador por cada volcán en el archivo.
for lat, lon, elev, name in zip(latitudes, longitudes, elevations, names):
    # Crear un popup personalizado para cada volcán.
    popup_content = html_template % (name, name, elev)
    iframe = folium.IFrame(html=popup_content, width=200, height=100)

    # Añadir un marcador circular en la ubicación del volcán, con el color según su elevación.
    fg_volcanes.add_child(folium.CircleMarker(
        location=[lat, lon],
        radius=10,
        popup=folium.Popup(iframe),
        color=color_volcan(elev),
        fill=True,
        fill_color=color_volcan(elev),
        fill_opacity=0.6
    ))

# Crear un grupo de características para la capa de población mundial.
fg_poblacion = folium.FeatureGroup(name="Población")

# Añadir una capa de polígonos del mapa mundial con colores según la población.
# Colores: verde (<10 millones), naranja (10-20 millones), rojo (>20 millones)
fg_poblacion.add_child(folium.GeoJson(
    data=open('App - Mapas/world.json', 'r', encoding='utf-8-sig').read(),
    style_function=lambda x: {
        'fillColor': 'green' if x['properties']['POP2005'] < 10000000 
                    else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000 
                    else 'red'
    }
))

# Añadir los grupos de características (volcanes y población) al mapa.
mapa.add_child(fg_volcanes)
mapa.add_child(fg_poblacion)

# Añadir un control de capas para permitir alternar entre las capas de volcanes y población.
mapa.add_child(folium.LayerControl())

# Guardar el mapa en un archivo HTML.
mapa.save("App - Mapas/Mapa.html")
