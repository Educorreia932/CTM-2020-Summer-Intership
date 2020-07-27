import folium
import gwp
import webbrowser

def plot(faps, dronekit_api, PT, UAV_location):
    home_location = dronekit_api.global_home_location
    
    lat = home_location.lat
    lon = home_location.lon
    
    m = folium.Map(
        location = [lat, lon],
        zoom_start = 30,
        tiles = 'Stamen Terrain'
    )
    
    # Represent FAPs
    for fap in faps:
        fap_coordinates = dronekit_api.get_location_metres(home_location, float(fap.x), float(fap.y))
        
        lat = fap_coordinates.lat
        lon = fap_coordinates.lon
        
        location = [lat, lon]
        
        folium.Marker(
            location,
            tooltip = fap.id,
            icon = folium.Icon(color = "blue")
        ).add_to(m)    
    
        radius = gwp.calculate_radius(PT, fap.snr)
    
        folium.Circle(
              location = location,
              radius = radius,
              color = 'crimson',
              fill = True,
              fill_color = 'crimson'
        ).add_to(m)
        
    # Represent UAV Relay
    x = UAV_location[0]
    y = UAV_location[1]
    uav_coordinates = dronekit_api.get_location_metres(home_location, x, y)
    
    location = [uav_coordinates.lat, uav_coordinates.lon]
    
    folium.Marker(
        location,
        tooltip = "UAV Relay",
        icon = folium.Icon(color = "red")
    ).add_to(m)    
    
    m.save('index.html')
    
    webbrowser.open('index.html', new = 2)