from context import Scheduler, SimpleBattery, Router, Point, Start, Charger, Destination, AddressInfo, TripBuilder, RoundHalfUpToInt

class EvScheduleIntegrationTest:
    def __init__(self):
        self.RouteBuilder = Router()
        self.TripBuilder = TripBuilder()

    def BuildTrip(self, name, stops, time, battery):
        time = time
        for c in stops[1:]:
            time += abs(c.AddressInfo.Latitude - stops[stops.index(c) - 1].AddressInfo.Latitude)

        return self.TripBuilder.BuildTestTrip(name, stops, time,  SimpleBattery(battery))

    def BuildSimpleTestCase(self, name, numberOfStops, time, battery, destinationHasCharger):
        route = [Point(AddressInfo(lat=0, long=0, title="Start"))]
        if destinationHasCharger:
            chargers = self.RouteBuilder.GetTestChargersInOrder(numberOfStops)
        else:
            chargers = self.RouteBuilder.GetTestChargersInOrder(numberOfStops - 1)
            chargers.append(Point(AddressInfo(lat=1,long=1, title="End")))

        route.extend(chargers)

        return self.BuildTrip(name, route, time, battery)

    def BuildRandomTestCase(self, name, numberOfStops, time, battery, destinationHasCharger):
        route = [Point(AddressInfo(lat=0, long=0, title="Start"))]

        if destinationHasCharger:
            chargers = self.RouteBuilder.GetTestChargersInOrder(numberOfStops)
        else:
            chargers = self.RouteBuilder.GetTestChargersInOrder(numberOfStops - 1)
            chargers.append(Point(AddressInfo(lat=1,long=1, title="End")))

        route.extend(chargers)

        return self.BuildTrip(name, route, RoundHalfUpToInt(time * 1.25), battery)

    def GetTestCases(self):
        """ Method used to return test cases for testing the optimizer. 

            Test cases should be in the following format:
            [Name, [stops], tripTime, battery]

            Stops is a list of possible stop along a route including the start and destination. 

            trip time is an integer. 

            battery is the battery level
        """
        testCases = []

        # Simple Test Case with Charger at end
        trip = self.BuildSimpleTestCase("Test Case 1", 3, 2, 4, True)
        testCases.append(trip)

        # Simple Test Case with Charger not at end
        trip = self.BuildSimpleTestCase("Test Case 2", 3, 2, 4, False)
        testCases.append(trip)

        # Simple Test Case with Random Chargers and Charger at end
        trip = self.BuildRandomTestCase("Random Case with Destination Charger", 10, 0, 40, True)
        testCases.append(trip)

        # Simple Test Case with Random Chargers and Charger not at end
        trip = self.BuildRandomTestCase("Random Case without Destination Charger", 10, 0, 40, False)
        testCases.append(trip)

        return testCases

    def Run(self):
        testCases = self.GetTestCases()
        scheduler = Scheduler()
        schedules = scheduler.ScheduleRoutes(testCases, True)
        
        for schedule in schedules:
            print schedule

if __name__ == '__main__':
    tester = EvScheduleIntegrationTest()
    tester.Run()