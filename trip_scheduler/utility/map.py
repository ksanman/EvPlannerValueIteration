import folium
import webbrowser

class Map:
    def __init__(self):
        pass

    def DrawRoute(self, route, chargers):
        """
        Draw a route on an OSM map and display the charging points on top of it. 
        """
        # Create the map and add the line
        print('Drawing route')
        m = folium.Map(location=[41.9, -97.3], zoom_start=4)
        polyline = folium.PolyLine(locations=route,weight=5)
        m.add_child(polyline)

        for point in chargers:
            folium.Marker(location=[point.AddressInfo.Latitude, point.AddressInfo.Longitude], popup=point.AddressInfo.Title).add_to(m)

        filepath = 'temp/map.html'
        m.save(filepath)
        #webbrowser.open(filepath)