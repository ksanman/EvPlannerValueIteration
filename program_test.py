from scheduler import Scheduler
from battery import NissanLeafBattery

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

    testCases = []

    # Test Case 1: [[1 Start Location, 1 Charger, 1 Destination with Charger], 3 time units, NissanLeaf with capacity of 3]
    testCases.append([
        "Test Case with final charging location.",
        [
            [0,0],
            [-3,1],
            [-5,1, True]
        ],
        10,
        NissanLeafBattery(10)
    ])


    # Test Case 2: [[1 Start Location, 1 Charger, 1 Destination without Charger] 3 time units, NissanLeaf with capacity of 3]
    testCases.append([
        "Test Case without final charging location.",
        [
            [0,0],
            [-3,1],
            [-5,1, False]
        ],
        10,
        NissanLeafBattery(10)
    ])

    
    return testCases

def run():
    testCases = GetTestCases()
    scheduler = Scheduler()
    schedules = scheduler.ScheduleRoutes(testCases)
    
    for schedule in schedules:
        print schedule

if __name__ == '__main__':
    run()