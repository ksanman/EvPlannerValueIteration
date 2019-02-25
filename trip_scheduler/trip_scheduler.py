from trip_builder import Router
from trip_builder import TripBuilder
from location_objects import Point, Charger, AddressInfo, Connection
from optimizer import Optimizer

class TripScheduler:
    """ Main interface with the EV trip scheduler. 
    """
    def __init__(self, rewards):
        """ Creates a new trip scheduler that schedules an EV trip based on the passed in rewards functions. 
        """
        self.Router = Router()
        self.TripBuilder = TripBuilder()
        self.Optimizer = Optimizer(rewards)

    def ScheduleRoute(self, name, startPoint, endPoint, expectedTripTime, carBattery):
        """ Schedules a single route given a start point, end point, expected trip time, and a car battery. 

            Keyword arguments:

            name -- The name of the trip.
            startPoint -- A Point object representing the starting location of the trip. 
            endPoint -- A Point or Charger object representing the destination location. 
            expectedTripTime -- The expected time to complete the trip
            carBattery -- An object that represents the battery of the ev vehicle. 
        """
        raise Exception('Not implemented')

    def ScheduleRouteFromFiles(self, name, routeFilePath, chargerFilePath, expectedTripTime, carBattery, isDestinationCharger):
        """ Schedules a single route given a filel that contains the route, a file that contains the chargers along the route,
        the expected trip time, and a car battery. 

            Keyword arguments:

            name -- The name of the trip.
            startPoint -- A Point object representing the starting location of the trip. 
            endPoint -- A Point or Charger object representing the destination location. 
            expectedTripTime -- The expected time to complete the trip
            carBattery -- An object that represents the battery of the ev vehicle. 
            isDestinationCharger -- Flag to determine if the destination is a charging location
        """
        routeDict = self.Router.GetRouteFromFile(routeFilePath)
        chargers = self.Router.GetNearestChargersFromFile(chargerFilePath)
        routeCoordinates = routeDict['route']

        start = Point(AddressInfo(lat=routeCoordinates[0][0], long=routeCoordinates[0][1], title="Start"))

        if not isDestinationCharger:
            end = Point(AddressInfo(lat=routeCoordinates[-1][0], long=routeCoordinates[-1][1], title="End"))
            route = [start]
            route.extend(chargers)
            route.append(end)
        else:
            route = [start]
            route.extend(chargers)
            
        
        trip = self.TripBuilder.BuildTrip(name, route, routeCoordinates, expectedTripTime, carBattery)
        
        return self.Optimizer.OptimizeRoutes([trip])


    def ScheduleRoutes(self, routes):
        """ Schedules several routes that each have a start point, end point, expected trip time, and a car battery. 

            Keyword arguments:

            routes -- A list of routes that contain the following:
                name -- The name of the trip.
                startPoint -- A Point object representing the starting location of the trip. 
                endPoint -- A Point or Charger object representing the destination location. 
                expectedTripTime -- The expected time to complete the trip
                carBattery -- An object that represents the battery of the ev vehicle. 
        """
        schedules = []
        for route in routes:
            schedules.append(self.ScheduleRoute(*route))