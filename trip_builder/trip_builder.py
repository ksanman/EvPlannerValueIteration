from router import Router
from location_objects import Point
from environment import Start, Charger, Destination
from trip import Trip
from utility import roundHalfUpToInt

class TripBuilder:
    def __init__(self):
        self.Router = Router()

    def BuildTestTrip(self, name, route, expectedTripTime, carBattery):
        # Compute distances, time to travel, energy expended, etc. 
        stops = route[1:-1]
        startPoint = route[0]
        endPoint = route[-1]

        route = [Start(startPoint.AddressInfo.Title, startPoint.AddressInfo)]
        
        for stop in stops:
                route.append(self.GetTestCharger(stop, stops[stops.index(stop) - 1], carBattery))

        route.append(self.GetTestDestination(endPoint, stops[stops.index(stop) - 1], carBattery))

        # Package the trip object. 
        trip = Trip(name, route, expectedTripTime, carBattery)

        # Return the trip object. 
        return trip

    def BuildTrip(self, name, route, expectedTripTime, carBattery):
        # Compute distances, time to travel, energy expended, etc. 
        stops = route[1:-2]
        startPoint = route[0]
        endPoint = route[-1]

        route = [Start(startPoint.addressInfo.Title, startPoint.addressInfo)]
        
        route = []
        for stop in stops:
                route.append(self.GetCharger(stop, stops[stops.index(stop) - 1], carBattery))

        route.extend(self.GetDestination(endPoint, stops[stops.index(stop) - 1], carBattery))

        # Package the trip object. 
        trip = Trip(name, route, expectedTripTime, carBattery)

        # Return the trip object. 
        return trip

    def GetStopsFromRoute(self, route, carBattery):
        stops = [Start(route[0].Title, route[0].AddressInfo)]

        for stop in route[1:-2]:
            stops.append(self.GetCharger(stop, route[route.index(stop) - 1], carBattery))

    def GetDestination(self, endPoint, previousLocation , carBattery):
        distance, duration, expendedEnergy = self.GetDistanceDurationAndExpendedEnergy(endPoint, previousLocation, carBattery)

        if type(endPoint) is Point:
            return Destination(expendedEnergy, duration, distance, endPoint.AddressInfo.Title, endPoint.AddressInfo, False)
        else:
            if endPoint.Connections[0].PowerKw:
                load = endPoint.Connections[0].PowerKw
            else:
                load = self.CalculateLoad(endPoint.Connections[0].Voltage,endPoint.Connections[0].Amps)
        
            return Destination(expendedEnergy, duration, distance, endPoint.AddressInfo.Title, endPoint.AddressInfo, True, load=load)

    def GetCharger(self, currentStop, previousStop, battery):
        distance, duration, expendedEnergy = self.GetDistanceDurationAndExpendedEnergy(currentStop, previousStop, battery)
   
        if currentStop.Connections[0].PowerKw:
            load = currentStop.Connections[0].PowerKw
        else:
            load = self.CalculateLoad(currentStop.Connections[0].Voltage, currentStop.Connections[0].Amps)

        return Charger(expendedEnergy, duration, distance, currentStop.AddressInfo.Title, currentStop.AddressInfo, load=load)

    def GetTestDestination(self, endPoint, previousLocation , carBattery):
        distance, duration, expendedEnergy = self.GetTestDistanceDurationAndExpendedEnergy(endPoint, previousLocation, carBattery)

        if isinstance(endPoint, Point):
            return Destination(expendedEnergy, duration, distance, endPoint.AddressInfo.Title, endPoint.AddressInfo, False)
        else:
            if endPoint.Connections[0].PowerKw:
                load = endPoint.Connections[0].PowerKw
            else:
                load = self.CalculateLoad(endPoint.Connections[0].Voltage,endPoint.Connections[0].Amps)
        
            return Destination(expendedEnergy, duration, distance, endPoint.AddressInfo.Title, endPoint.AddressInfo, True, load=load)

    def GetTestCharger(self, currentStop, previousStop, battery):
        distance, duration, expendedEnergy = self.GetTestDistanceDurationAndExpendedEnergy(currentStop, previousStop, battery)
   
        if currentStop.Connections[0].PowerKw:
            load = currentStop.Connections[0].PowerKw
        else:
            load = self.CalculateLoad(currentStop.Connections[0].Voltage, currentStop.Connections[0].Amps)

        return Charger(expendedEnergy, duration, distance, currentStop.AddressInfo.Title, currentStop.AddressInfo, load=load)

    def GetDistanceDurationAndExpendedEnergy(self, currentStop, previousStop, battery):
        distance, duration = self.Router.GetDistanceAndDurationBetweenPoints(currentStop, previousStop)
        expendedEnergy = battery.Discharge(duration)

        distance = roundHalfUpToInt(distance)
        duration = roundHalfUpToInt(duration)
        expendedEnergy = roundHalfUpToInt(expendedEnergy)

        return (distance, duration, expendedEnergy)

    def GetTestDistanceDurationAndExpendedEnergy(self, currentStop, previousStop, battery):
        distance = duration = abs(previousStop.AddressInfo.Latitude - currentStop.AddressInfo.Latitude)
        expendedEnergy = battery.Discharge(duration)

        distance = roundHalfUpToInt(distance)
        duration = roundHalfUpToInt(duration)
        expendedEnergy = roundHalfUpToInt(expendedEnergy)

        return (distance, duration, expendedEnergy)

    def CalculateLoad(self, voltage, current):
        return (voltage * current) / 1000

