from ev_trip_scheduler_env import EvTripScheduleEnvironment
from value_interation_agent import ValueIterationAgent
from stop import Start, Charger, Destination
from battery import NissanLeafBattery

def CreateRoute(stops):
    """ This method will eventually parse a list of lat/long coordinates and charger information to 
        create the route object. 
        
        It will be able to dynamically allocate the expended energy and duration to each stop. 
    """    
    route = [Start()]
    for stop in range(len(stops) - 1):
        route.append(Charger(stops[stop][0], stops[stop][1]))
    route.append(Destination(stops[-1][0], stops[-1][1], stops[-1][2]))
    return route

def main():
    # Define the environment and create it. 

    # Define the test environment. 
    stops = [
        [-1,1], 
        [-1,1], 
        [-1,1, True]
    ]
    time = 3
    battery = 4
    isPrintStats = True


    # This is a route object, that contains information about the ev vehicles route. 
    route = CreateRoute(stops)

    # Time object
    expectedTimeToDestination = time

    # Battery Object
    battery = NissanLeafBattery(battery)

    environment = EvTripScheduleEnvironment(route, expectedTimeToDestination, battery, True)

    # Build the value table
    agent = ValueIterationAgent(environment)
    agent.PerformValueIteration(isPrintStats)
    agent.FindOptimalPolicy(isPrintStats)

    # Evaluate
    agent.EvaluatePolicy(1, False, isPrintStats)

    # Display Graphs
    agent.DisplayEvaluationGraphs()



if __name__ == '__main__':
    main()