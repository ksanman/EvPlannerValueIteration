from ..location_objects import ChargerContext, Charger as DbCharger, Connection, AddressInfo, Point
from ..utility import ConvertFromSecondsToFifteenMinuteBlock
import random
import requests
import json
import polyline

class Router:
    def __init__(self):
        self.RouteRequestString = 'http://router.project-osrm.org/route/v1/driving/{0},{1};{2},{3}?overview=full&steps=true'
        self.DistanceRequestString = 'http://router.project-osrm.org/route/v1/driving/{0},{1};{2},{3}?overview=simplified'       
        self.ChargerContext = ChargerContext()

        self.ShortTestChargerList = [
            DbCharger(AddressInfo(ID=1, lat=1, long=1, title="Charger{0}".format(1)), [Connection(amps=63,voltage=400)]),
            DbCharger(AddressInfo(ID=2, lat=2, long=2, title="Charger{0}".format(2)), [Connection(amps=63,voltage=400)]),
            DbCharger(AddressInfo(ID=3, lat=3, long=3, title="Charger{0}".format(3)), [Connection(amps=63,voltage=400)]),
            DbCharger(AddressInfo(ID=4, lat=4, long=4, title="Charger{0}".format(4)), [Connection(amps=63,voltage=400)]),
        ]

        self.LongTestChargerList = [
            DbCharger(AddressInfo(ID=1, lat=1, long=1, title="Charger{0}".format(1)), [Connection(amps=63,voltage=400)]),
            DbCharger(AddressInfo(ID=2, lat=2, long=2, title="Charger{0}".format(2)), [Connection(amps=63,voltage=400)]),
            DbCharger(AddressInfo(ID=3, lat=3, long=3, title="Charger{0}".format(3)), [Connection(amps=63,voltage=400)]),
            DbCharger(AddressInfo(ID=4, lat=4, long=4, title="Charger{0}".format(4)), [Connection(amps=63,voltage=400)]),
            DbCharger(AddressInfo(ID=5, lat=5, long=5, title="Charger{0}".format(5)), [Connection(amps=63,voltage=400)]),
            DbCharger(AddressInfo(ID=6, lat=2, long=2, title="Charger{0}".format(6)), [Connection(amps=63,voltage=400)]),
            DbCharger(AddressInfo(ID=7, lat=3, long=3, title="Charger{0}".format(7)), [Connection(amps=63,voltage=400)]),
            DbCharger(AddressInfo(ID=8, lat=4, long=4, title="Charger{0}".format(8)), [Connection(amps=63,voltage=400)]),
            DbCharger(AddressInfo(ID=9, lat=10, long=1, title="Charger{0}".format(9)), [Connection(amps=63,voltage=400)]),
            DbCharger(AddressInfo(ID=10, lat=9, long=2, title="Charger{0}".format(10)), [Connection(amps=63,voltage=400)]),
            DbCharger(AddressInfo(ID=11, lat=8, long=3, title="Charger{0}".format(11)), [Connection(amps=63,voltage=400)]),
            DbCharger(AddressInfo(ID=12, lat=6, long=4, title="Charger{0}".format(12)), [Connection(amps=63,voltage=400)]),
            DbCharger(AddressInfo(ID=13, lat=6, long=1, title="Charger{0}".format(13)), [Connection(amps=63,voltage=400)]),
            DbCharger(AddressInfo(ID=14, lat=5, long=2, title="Charger{0}".format(14)), [Connection(amps=63,voltage=400)]),
            DbCharger(AddressInfo(ID=15, lat=9, long=3, title="Charger{0}".format(15)), [Connection(amps=63,voltage=400)]),
            DbCharger(AddressInfo(ID=16, lat=4, long=4, title="Charger{0}".format(16)), [Connection(amps=63,voltage=400)]),
            DbCharger(AddressInfo(ID=17, lat=8, long=4, title="Charger{0}".format(17)), [Connection(amps=63,voltage=400)]),
            DbCharger(AddressInfo(ID=18, lat=6, long=1, title="Charger{0}".format(18)), [Connection(amps=63,voltage=400)]),
            DbCharger(AddressInfo(ID=19, lat=2, long=2, title="Charger{0}".format(19)), [Connection(amps=63,voltage=400)]),
            DbCharger(AddressInfo(ID=20, lat=1, long=3, title="Charger{0}".format(20)), [Connection(amps=63,voltage=400)]),
            DbCharger(AddressInfo(ID=21, lat=1, long=4, title="Charger{0}".format(21)), [Connection(amps=63,voltage=400)])
        ]

    def BuildRoute(self, name, startPoint, endPoint, searchDistance):
        """ Given a start point and an end point, this method will build a route as a list of possible charging stops from the start point to the
            end point. 

            Keyword arguments: 

            startPoint -- A Point object consisting of the starting location. 
            endPoint -- A Point object consisting of the destination location. 
            searchDistance -- The radius to search from the route for charging locations.
        """
        osrmRoute = self.GetRouteFromOsrm(startPoint, endPoint)
        nearestChargers = self.GetNearestChargersFromDatabase(osrmRoute['route'], searchDistance)

        route = [startPoint]
        route.extend(nearestChargers)
        route.append(endPoint)

        return {'ScheduleRoute': route, 'Polyline': osrmRoute['route'], 'ChargingPoints': nearestChargers}

    def GetRouteFromOsrm(self, start, end):
        """ Submits a request to OSRM to get a route data. All that are needed are the start coordinates
            and the end coordinates in latitude, longitude pairs. 
        """

        print 'Getting route...'
        urlRequest = self.RouteRequestString.format(start.Longitude, start.Latitude, end.Longitude, end.Latitude)
        response = requests.get(urlRequest)
        content = response.content 
        jsonData = content.decode('utf8').replace("'", '"')
        print 'Route recieved.'
        # Load the JSON to a Python list & dump it back out as formatted JSON
        data = json.loads(jsonData)
        return self.GetRouteFromJson(data)

    def GetRouteFromFile(self, filePath):
        """ Loads a .json file containing a OSRM route response and constructs a route from the data. 
        """
        with open(filePath, 'r') as file:
            content = file.read()

        jsonData = content.decode('utf8').replace("'", '"')
        data = json.loads(jsonData)
        return self.GetRouteFromJson(data)

    def GetRouteFromJson(self, data):
        """
        Build a route from json data. 
        Returns the route coordinates as well as all intersections along the route. 
        """
        route = data["routes"][0]
        print 'Building Route'
        #get the intersections along the route
        intersections = self.GetIntersections(route)


        return {'route':polyline.decode(route['geometry']),'intersections':intersections}

    def GetIntersections(self, data):
        """
        Get all the intersections along the route.
        """
        intersections = []
        for l in data['legs']:
            for s in l['steps']:
                for i in s['intersections']:
                    location = i['location']
                    intersections.append(Point(AddressInfo(lat=location[1], long=location[0])))

        return intersections

    def GetNearestChargersFromDatabase(self, route, searchDistance):
        """ Gets the charger objects within the search distance of the route from the database.
             
            Keyword arguments:

            route -- A list of lat/long pairs that resemble the route. 
            searchDistance -- The radius to search from the route for charging locations.
        """
        raise Exception("Not Implemented")


    def GetNearestChargersFromFile(self, filePath):
        """ Gets the charger objects for a route from a file.

            Keyword arguments:

            filePath -- the location of the file containing the charger contents. 
        """ 
        chargers = self.ChargerContext.GetChargersFromFile(filePath)
        return chargers

    def GetDistanceAndDurationBetweenPoints(self, point1, point2):
        """ Get the distance and travel time between two lat/long points by traveling on a road. 
            Distance is returned in km, 
            Time is returned in time blocks of 15 minutes. 
        """
        request = self.DistanceRequestString.format(point1.AddressInfo.Longitude, point1.AddressInfo.Latitude, point2.AddressInfo.Longitude, point2.AddressInfo.Latitude)
        r = requests.get(request)
        c = r.content 
        my_json = c.decode('utf8').replace("'", '"')
        data = json.loads(my_json)
        route = data["routes"][0]
        distance = float(route["distance"]) / 1000
        duration = ConvertFromSecondsToFifteenMinuteBlock(float(route['duration']))
        return distance, duration

    def GetTestChargersInOrder(self, numberOfChargers):
        if numberOfChargers < len(self.ShortTestChargerList):
            return self.ShortTestChargerList[:numberOfChargers]
        else:
            return self.LongTestChargerList[:numberOfChargers]