from scheduler import Scheduler
from battery import NissanLeafBattery
from route_builder import RouteBuilder
from charger_info import Point
from decimal import Decimal, ROUND_HALF_UP

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
    routeBuilder = RouteBuilder()


    testCases = []

    # # Simple Test Case with Charger at end
    # chargers = routeBuilder.GetChargersInOrder(4)
    # route = [Point("Start", 0, 0)]
    # route.extend(chargers)
    # time = 1
    # for stop in route[1:]:
    #     _, t = GetDistanceAndTime(route[route.index(stop) - 1], stop)
    #     time += t
    
    # testCases.append([
    #     "Test Case 1",
    #     route, 
    #     time, 
    #     NissanLeafBattery(4)
    # ])

    # # Simple Test Case with Charger not at end
    # chargers = routeBuilder.GetChargersInOrder(3)
    # route = [Point("Start", 0, 0)]
    # route.extend(chargers)
    # route.append(Point("End", 4, 4))
    # time = 1
    # for stop in route[1:]:
    #     _, t = GetDistanceAndTime(route[route.index(stop) - 1], stop)
    #     time += t
    
    
    # testCases.append([
    #     "Test Case 2",
    #     route, 
    #     time, 
    #     NissanLeafBattery(4)
    # ])

    # Simple Test Case with Random Chargers
    chargers = routeBuilder.GetRandomSample(10)
    route = [Point("Start", 0, 0)]
    route.extend(chargers)
    time = 0
    for stop in route[1:]:
        _, t = GetDistanceAndTime(route[route.index(stop) - 1], stop)
        time += t
    
    time = int(Decimal(time * 1.25).quantize(Decimal('0'), rounding=ROUND_HALF_UP))
    
    testCases.append([
        "",
        route, 
        time, 
        NissanLeafBattery(40)
    ])


    return testCases

def run():
    testCases = GetTestCases()
    scheduler = Scheduler()
    schedules = scheduler.ScheduleRoutes(testCases, True)
    
    for schedule in schedules:
        print schedule

def GetDistanceAndTime(point1, point2):
    """ Return the distance and time to travel the distance. 
        This will be replaced with OSRM when integrating. 
    """
    d1 = abs(point2.Latitude - point1.Latitude)
    # For future distance calculations. 
    #d2 = point2.Longitude - point1.Longitude
    return d1, d1

if __name__ == '__main__':
    run()