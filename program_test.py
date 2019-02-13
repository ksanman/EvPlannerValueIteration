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

    # Test Case 1: [[1 Start Location, 1 Charger, 1 Destination with Charger], 10 time units, NissanLeaf with capacity of 10]
    # testCases.append([
    #     "Test Case with final charging location.",
    #     [
    #         [0,0],
    #         [-3,1],
    #         [-5,1, True]
    #     ],
    #     10,
    #     NissanLeafBattery(10)
    # ])


    # # Test Case 2: [[1 Start Location, 1 Charger, 1 Destination without Charger] 10 time units, NissanLeaf with capacity of 10]
    # testCases.append([
    #     "Test Case without final charging location.",
    #     [
    #         [0,0],
    #         [-3,1],
    #         [-5,1, False]
    #     ],
    #     10,
    #     NissanLeafBattery(10)
    # ])

    # Test Case 3: [[1 Start Location, 20 Chargers, 1 Destination with Charger]  20 time units, NissanLeaf with capacity of 10]
    # Investigate why this case doesn't work. 
    # The car should stop at stop 7 or 8 and charge until 80% full. 
    testCases.append([
        "Test Case without final charging location.",
        [
            [0,0],
            [-1,1],
            [-1,1],
            [-1,1],
            [-1,1],
            [-1,1],
            [-1,1],
            [-3,3],
            [-6,6],
            [-1,1],
            [-5,5, True]
        ],
        25,
        NissanLeafBattery(10)
    ])


    return testCases

def run():
    testCases = GetTestCases()
    scheduler = Scheduler()
    schedules = scheduler.ScheduleRoutes(testCases, True)
    
    for schedule in schedules:
        print schedule

if __name__ == '__main__':
    run()