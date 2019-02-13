from ev_trip_scheduler_env import EvTripScheduleEnvironment
from value_interation_agent import ValueIterationAgent
from stop import Start, Charger, Destination
from battery import NissanLeafBattery

class Optimizer:
    def OptimizeRoute(self, routeName, route, battery, expectedTimeToDestination, isPrintStats):
        """
            Given a route, a car battery, and an expected arrival time, find the optimal charging location schedule and return it. 

            Keyword arguments:

            route -- A list of possible charging points during the trip. Each charging point contains information about that location, how long it took to get there 
                    from the previous location, and how much energy was expended to reach the location. 
            battery -- A model of the EV car battery for calculating charging and discharging rates. 
            expectedTimeToDestination -- The expected time to reach the destination. 
            isPrintStats -- Boolean value that triggers printing the optimizer output to the console. 
        """

        environment = EvTripScheduleEnvironment(route, expectedTimeToDestination, battery)

        # Build the value table
        agent = ValueIterationAgent(environment)
        agent.PerformValueIteration(isPrintStats)
        agent.FindOptimalPolicy(isPrintStats)

        # Evaluate
        agent.EvaluatePolicy(1, False, isPrintStats)

        # Display Graphs
        agent.DisplayEvaluationGraphs(routeName)

        return agent.GetSchedule()