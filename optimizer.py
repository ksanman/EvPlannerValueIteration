from ev_trip_scheduler_env import EvTripScheduleEnvironment
from value_interation_agent import ValueIterationAgent
from stop import Start, Charger, Destination
from battery import NissanLeafBattery

def CreateRoute():
    """ This method will eventually parse a list of lat/long coordinates and charger information to 
        create the route object. 
        
        It will be able to dynamically allocate the expended energy and duration to each stop. 

        Currently, the objects must be hard coded. 
    """    
    route = [Start(), Charger(-1, 1), Destination(-1, 1, True)]
    return route    

def main():
    # Define the environment and create it. 
    
    # This is a route object, that contains information about the ev vehicles route. 
    route = CreateRoute()

    # Time object
    expectedTimeToDestination = 3

    # Battery Object
    battery = NissanLeafBattery(3)

    environment = EvTripScheduleEnvironment(route, expectedTimeToDestination, battery, True)

    # Build the value table
    agent = ValueIterationAgent(environment)
    agent.PerformValueIteration()
    agent.PrintVTable()
    agent.FindOptimalPolicy()
    agent.PrintPolicy()

    # Evaluate
    agent.EvaluatePolicy(1, False)

    # Display Graphs
    agent.DisplayEvaluationGraphs()



if __name__ == '__main__':
    main()