from router import Router
from ..location_objects import Point, AddressInfo
from ..environment import Start, Charger, Destination
from trip import Trip
from ..utility import RoundHalfUpToInt

class TripBuilder:
    def __init__(self):
        self.Router = Router()

    def BuildTestTrip(self, name, route, polyline, expectedTripTime, carBattery):
        # Compute distances, time to travel, energy expended, etc. 
        stops = route[1:-1]
        startPoint = route[0]
        endPoint = route[-1]

        tripRoute = [Start(startPoint.AddressInfo.Title, startPoint.AddressInfo)]
        
        for stop in stops:
                tripRoute.append(self.GetTestCharger(stop, route[route.index(stop) - 1], carBattery))

        tripRoute.append(self.GetTestDestination(endPoint, route[-2], carBattery))

        # Package the trip object.  
        trip = Trip(name, tripRoute, polyline, expectedTripTime, carBattery)

        # Return the trip object. 
        return trip

    def BuildTrip(self, name, route, polyline, expectedTripTime, carBattery):
        # Compute distances, time to travel, energy expended, etc. 
        stops = route[1:-1]
        startPoint = route[0]
        endPoint = route[-1]

        tripRoute = [Start(startPoint.AddressInfo.Title, startPoint.AddressInfo)]
        
        for stop in stops:
                tripRoute.append(self.GetCharger(stop, route[route.index(stop) - 1], carBattery))

        tripRoute.append(self.GetDestination(endPoint, route[-2], carBattery))

        # Package the trip object. 
        trip = Trip(name, tripRoute, polyline, expectedTripTime, carBattery)

        # Return the trip object. 
        return trip

    def GetDestination(self, endPoint, previousLocation , carBattery):
        distance, duration, expendedEnergy = self.GetDistanceDurationAndExpendedEnergy(endPoint, previousLocation, carBattery)

        if type(endPoint) is Point:
            return Destination(expendedEnergy, duration, distance, endPoint.AddressInfo.Title, endPoint.AddressInfo, 0,False)
        else:
            distanceFromIntersection, _ = self.Router.GetDistanceAndDurationBetweenPoints(endPoint, Point(AddressInfo(lat=endPoint.IntersectionLatitude, long=endPoint.IntersectionLongitude)))

            if endPoint.Connections[0].PowerKw:
                load = endPoint.Connections[0].PowerKw
            else:
                load = self.CalculateLoad(endPoint.Connections[0].Voltage,endPoint.Connections[0].Amps)
        
            return Destination(expendedEnergy, duration, distance, endPoint.AddressInfo.Title, endPoint.AddressInfo, True, distanceFromIntersection, load)

    def GetCharger(self, currentStop, previousStop, battery):
        distance, duration, expendedEnergy = self.GetDistanceDurationAndExpendedEnergy(currentStop, previousStop, battery)
        distanceFromIntersection, _ = self.Router.GetDistanceAndDurationBetweenPoints(currentStop, Point(AddressInfo(lat=currentStop.IntersectionLatitude, long=currentStop.IntersectionLongitude)))

        if currentStop.Connections[0].PowerKw:
            load = currentStop.Connections[0].PowerKw
        else:
            load = self.CalculateLoad(currentStop.Connections[0].Voltage, currentStop.Connections[0].Amps)

        return Charger(expendedEnergy, duration, distance, currentStop.AddressInfo.Title, currentStop.AddressInfo,distanceFromIntersection,load)

    def GetTestDestination(self, endPoint, previousLocation , carBattery):
        distance, duration, expendedEnergy = self.GetTestDistanceDurationAndExpendedEnergy(endPoint, previousLocation, carBattery)

        if isinstance(endPoint, Point):
            return Destination(expendedEnergy, duration, distance, endPoint.AddressInfo.Title, endPoint.AddressInfo, 0,False)
        else:
            if endPoint.Connections[0].PowerKw:
                load = endPoint.Connections[0].PowerKw
            else:
                load = self.CalculateLoad(endPoint.Connections[0].Voltage,endPoint.Connections[0].Amps)
        
            return Destination(expendedEnergy, duration, distance, endPoint.AddressInfo.Title, endPoint.AddressInfo, True, 0, load)

    def GetTestCharger(self, currentStop, previousStop, battery):
        distance, duration, expendedEnergy = self.GetTestDistanceDurationAndExpendedEnergy(currentStop, previousStop, battery)
   
        if currentStop.Connections[0].PowerKw:
            load = currentStop.Connections[0].PowerKw
        else:
            load = self.CalculateLoad(currentStop.Connections[0].Voltage, currentStop.Connections[0].Amps)

        return Charger(expendedEnergy, duration, distance, currentStop.AddressInfo.Title, currentStop.AddressInfo, 0,load)

    def GetDistanceDurationAndExpendedEnergy(self, currentStop, previousStop, battery):
        distance, duration = self.Router.GetDistanceAndDurationBetweenPoints(currentStop, previousStop)
        expendedEnergy = battery.Discharge(duration, distance)

        distance = RoundHalfUpToInt(distance)
        duration = RoundHalfUpToInt(duration)
        expendedEnergy = RoundHalfUpToInt(expendedEnergy)

        return (distance, duration, expendedEnergy)

    def GetTestDistanceDurationAndExpendedEnergy(self, currentStop, previousStop, battery):
        distance = duration = abs(previousStop.AddressInfo.Latitude - currentStop.AddressInfo.Latitude)
        expendedEnergy = battery.Discharge(duration, distance)

        distance = RoundHalfUpToInt(distance)
        duration = RoundHalfUpToInt(duration)
        expendedEnergy = RoundHalfUpToInt(expendedEnergy)

        return (distance, duration, expendedEnergy)

    def CalculateLoad(self, voltage, current):
        return (voltage * current) / 1000

