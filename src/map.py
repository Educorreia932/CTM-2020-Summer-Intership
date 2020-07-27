import folium
import json
import requests

m = folium.Map(
    location=[45.372, -121.6972],
    zoom_start=12,
    tiles='Stamen Terrain'
)

tooltip = 'Click me!'

folium.Marker([45.3288, -121.6625], popup='<i>Mt. Hood Meadows</i>', tooltip=tooltip).add_to(m)
folium.Marker([45.3311, -121.7113], popup='<b>Timberline Lodge</b>', icon=folium.Icon(color="red"), tooltip=tooltip).add_to(m)

folium.Circle(
      location=[45.3288, -121.6625],
      radius= 10000,
      color='crimson',
      fill=True,
      fill_color='crimson'
   ).add_to(m)

m.save('index.html')