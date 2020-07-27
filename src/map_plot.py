import folium
import webbrowser

def plot(faps, dronekit_api):
    home_location = dronekit_api.global_home_location
    
    lat = home_location.lat
    lon = home_location.lon
    
    m = folium.Map(
        location = [lat, lon],
        zoom_start = 12,
        tiles = 'Stamen Terrain'
    )
    
    for fap in faps:
        fap_coordinates = dronekit_api.get_location_metres(home_location, float(fap.x), float(fap.y))
        
        lat = fap_coordinates.lat
        lon = fap_coordinates.lon
        
        folium.Marker([lat, lon], tooltip = fap.id).add_to(m)    
    
    # folium.Circle(
    #       location = [45.3288, -121.6625],
    #       radius = 10000,
    #       color = 'crimson',
    #       fill = True,
    #       fill_color = 'crimson'
    #    ).add_to(m)
    
    m.save('index.html')
    
    webbrowser.open('index.html', new = 2)