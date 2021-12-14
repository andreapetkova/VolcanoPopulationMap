import folium
import pandas

data = pandas.read_csv("Volcanoes.txt")
lat = list(data["LAT"])
lon = list(data["LON"])
elev = list(data["ELEV"])
name = list(data["NAME"])


def color_producer(elevation):
    if elevation < 1000:
        return "green"
    elif 1000 <= elevation <= 3000:
        return "orange"
    else:
        return "red"


map_volcano = folium.Map(location=[38.58, -99.09], zoom_start=5, tiles="CartoDB Positron")

fgv = folium.FeatureGroup(name="Volcanoes")

for lt, ln, el, n in zip(lat, lon, elev, name):
    html = f"""
    <div style="font-family: century gothic; color: dark grey; font-size: 15px">
    <h4>Volcano info:</h4>
    Name = {n}
    <br>Height = {el} m
    </div>
    """

    iframe = folium.IFrame(html=html, width=200, height=100,)
    fgv.add_child(folium.CircleMarker(location=(lt, ln), radius=6, popup=folium.Popup(iframe),
                                      fill_color=color_producer(el), color="grey", fill_opacity=0.6))

fgp = folium.FeatureGroup(name="Population")
fgp.add_child(folium.GeoJson(data=open("world.json", "r", encoding="utf-8-sig").read(),
                             style_function=lambda x: {"fillColor": 'green' if x['properties']['POP2005'] < 10000000
                             else 'orange' if 10000000 <= x['properties']['POP2005'] < 50000000 else 'red'}))            #attaches yellow if the properties(value) of the pop2005 is less that 1000000


map_volcano.add_child(fgv)
map_volcano.add_child(fgp)
map_volcano.add_child(folium.LayerControl())

map_volcano.save("Mapl.html")
