from context import Scheduler, NissanLeafBattery, Router, Point, Start, Charger, Destination, AddressInfo, TripBuilder

def GetTestCases():
    """ Method used to return test cases for testing the optimizer. 

        Test cases should be in the following format:
        [Name, [stops], tripTime, battery]

        stops are in the form [energyExpendedFromPreviousStop, timeFromPreviousStop]
            The first element in the stop list is ignored for now, but will contain coordinates of the start location later. 
            Destination Locations must include the 'isDestinationCharger' flag. ex: [energyExpendedFromPreviousStop, timeFromPreviousStop, isDestinationCharger]

        trip time is an integer. 

        battery is a derivative of the Battery class from battery.py
    """
    routeBuilder = Router()
    tripBuilder = TripBuilder()

    testCases = []

    # Simple Test Case with Charger at end
    route = [Point(AddressInfo(lat=0, long=0, title="Start"))]
    chargers = routeBuilder.GetTestChargersInOrder(3)
    route.extend(chargers)

    time = 2
    for c in route[1:]:
        time += c.AddressInfo.Latitude - route[route.index(c) - 1].AddressInfo.Latitude

    trip = tripBuilder.BuildTestTrip("Test Case 1", route, time,  NissanLeafBattery(4))

    testCases.append(trip)

    # # Simple Test Case with Charger not at end
    route = [Point(AddressInfo(lat=0, long=0, title="Start"))]
    chargers = routeBuilder.GetTestChargersInOrder(2)
    route.extend(chargers)
    route.append(Point(AddressInfo(lat=3,long=3, title="End")))

    time = 2
    for c in route[1:]:
        time += c.AddressInfo.Latitude - route[route.index(c) - 1].AddressInfo.Latitude

    trip = tripBuilder.BuildTestTrip("Test Case 2", route, time,  NissanLeafBattery(4))

    testCases.append(trip)

    # Simple Test Case with Random Chargers
    # chargers = routeBuilder.GetTestRandomSample(10)
    # route = [Point("Start", 0, 0)]
    # route.extend(chargers)
    # time = 0
    # for stop in route[1:]:
    #     _, t = GetDistanceAndTime(route[route.index(stop) - 1], stop)
    #     time += t
    
    # time = int(Decimal(time * 1.25).quantize(Decimal('0'), rounding=ROUND_HALF_UP))
    
    # testCases.append([
    #     "",
    #     route, 
    #     time, 
    #     NissanLeafBattery(40)
    # ])


    return testCases

def run():
    testCases = GetTestCases()
    scheduler = Scheduler()
    schedules = scheduler.ScheduleRoutes(testCases, True)
    
    for schedule in schedules:
        print schedule

if __name__ == '__main__':
    run()