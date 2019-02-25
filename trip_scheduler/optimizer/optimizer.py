from ..environment import EvTripScheduleEnvironment
from value_interation_agent import ValueIterationAgent

class Optimizer:
    """ Provides methods to schedule the charging locations several EV trip routes. 
    """
    def __init__(self, rewardFunctions):
        """ Initializes a new optimizer class with the passed in reward functions interface. 

            Keyword arguments:

            rewardFunctions -- the reward functions to use for optimization. 
        """
        self.Rewards = rewardFunctions

    def OptimizeRoutes(self, routes, isPrintStats=False):
        """ Given a list of routes, find the optimal schedule for each on and return them. 
            
            Keywork arguments:
            
            routes --  A list of trips. 
        """
        schedules = []
        for trip in routes:
            schedules.append(self.OptimizeRoute(trip, isPrintStats))

        return schedules

    def OptimizeRoute(self, trip, isPrintStats):
        """
            Given a route, a car battery, and an expected arrival time, find the optimal charging location schedule and return it. 

            Keyword arguments:

            route -- A list of possible charging points during the trip. Each charging point contains information about that location, how long it took to get there 
                    from the previous location, and how much energy was expended to reach the location. 
            battery -- A model of the EV car battery for calculating charging and discharging rates. 
            expectedTimeToDestination -- The expected time to reach the destination. 
            isPrintStats -- Boolean value that triggers printing the optimizer output to the console. 
        """
        environment = EvTripScheduleEnvironment(trip.Route, trip.TripTime, trip.Battery, self.Rewards)

        # Build the value table
        agent = ValueIterationAgent(environment)
        agent.PerformValueIteration(isPrintStats)
        agent.FindOptimalPolicy(isPrintStats)

        # Evaluate
        agent.EvaluatePolicy(1, False, isPrintStats)

        # Display Graphs
        agent.DisplayEvaluationGraphs(trip.Name)

        return agent.GetSchedule(trip.Polyline)