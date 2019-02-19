from location_objects import ChargerContext, Charger as DbCharger, Connection, AddressInfo, Point
import random
import requests
import json
import polyline

class Router:
    def __init__(self):
        self.RouteRequestString = 'http://router.project-osrm.org/route/v1/driving/{0},{1};{2},{3}?overview=full&steps=true'
        self.DistanceRequestString = 'http://router.project-osrm.org/route/v1/driving/{0},{1};{2},{3}?overview=simplified'
        self.TestChargerList = []
        self.ChargerContext = ChargerContext()
        for c in range(1, 20):
            self.TestChargerList.append(DbCharger(AddressInfo(ID=c, lat=c, long=c, title="Charger{0}".format(c)), [Connection(amps=63,voltage=400)]))

    def BuildRoute(self, name, startPoint, endPoint, searchDistance):
        """ Given a start point and an end point, this method will build a route as a list of possible charging stops from the start point to the
            end point. 

            Keyword arguments: 

            startPoint -- A Point object consisting of the starting location. 
            endPoint -- A Point object consisting of the destination location. 
            searchDistance -- The radius to search from the route for charging locations.
        """
        osrmRoute = self.GetRouteFromOsrm(startPoint, endPoint)
        nearestChargers = self.GetNearestChargers(osrmRoute['route'], searchDistance)

        route = [startPoint]
        route.extend(nearestChargers)
        route.append(endPoint)

        return {'ScheduleRoute': route, 'Polyline': osrmRoute['route'], 'ChargingPoints': nearestChargers}

    def GetRouteFromOsrm(self, start, end):
        """
        Submits a request to OSRM to get a route data. All that are needed are the start coordinates
        and the end coordinates in latitude, longitude pairs. 
        """

        print('Getting route...')
        url_request = self.RouteRequestString.format(start.Longitude, start.Latitude, end.Longitude, end.Latitude)
        r = requests.get(url_request)
        c = r.content 
        my_json = c.decode('utf8').replace("'", '"')
        print('Route recieved.')
        # Load the JSON to a Python list & dump it back out as formatted JSON
        data = json.loads(my_json)
        return self.GetRouteFromJson(data)

    def GetRouteFromJson(self, data):
        """
        Build a route from json data. 
        Returns the route coordinates as well as all intersections along the route. 
        """
        route = data["routes"][0]
        print('building route')
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

    def GetNearestChargers(self, route, searchDistance):
        """ Gets the charger objects within the search distance of the route.

            Keyword arguments:

            route -- A list of lat/long pairs that resemble the route. 
            searchDistance -- The radius to search from the route for charging locations.
        """ 
        chargers = self.ChargerContext.GetChargersFromFile()
        return chargers

    def GetDistanceAndDurationBetweenPoints(self, point1, point2):
        """ Get the distance and travel time between two lat/long points by traveling on a road. 
        """
        request = self.DistanceRequestString.format(point1.Longitude, point1.Latitude, point2.Longitude, point2.Latitude)
        r = requests.get(request)
        c = r.content 
        my_json = c.decode('utf8').replace("'", '"')
        data = json.loads(my_json)
        route = data["routes"][0]
        distance = float(route["distance"])
        duration = float(route['duration'])
        return distance, duration

    def GetTestChargersInOrder(self, numberOfChargers):
        return self.TestChargerList[:numberOfChargers]

    def GetTestRandomSample(self, numberOfChargers):
        return random.sample(self.TestChargerList, numberOfChargers)