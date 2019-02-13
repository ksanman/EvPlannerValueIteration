from battery import NissanLeafBattery
from ev_trip_scheduler_env import EvTripScheduleEnvironment
from stop import Charger, Destination, Start
from value_interation_agent import ValueIterationAgent


class Trip:
    """ An object used to hold information about a particular trip. 
    """
    def __init__(self, name, route, tripTime, battery):
        self.Name = name
        self.Route = route
        self.TripTime = tripTime
        self.Battery = battery

class Scheduler:
    """ Provides methods to schedule the charging locations several EV trip routes. 
    """

    def ScheduleRoutes(self, routes, isPrintStats=False):
        """ Given a list of routes, find the optimal schedule for each on and return them. 
            
            Keywork arguments:
            
            routes --  A list of routes in the form [[StartPoint, chargers, ... ,destination], tripTime, and an EV battery object)]
            isPrintStats -- Boolean value that determins if diagnostics should be shown in the console. 
        """
        scheduledRoutes = self.BuildRoutes(routes)

        schedules = []
        for trip in scheduledRoutes:
            schedules.append(self.OptimizeRoute(trip.Name, trip.Route, trip.Battery, trip.TripTime, isPrintStats))

        return schedules

    def BuildRoutes(self, routes):
        """ Take the given routes and transform them into simple data that the environment can use. 
        """
        trips = []
        for route in routes:
            trips.append(self.BuildRoute(route))
        return trips


    def BuildRoute(self, route):
        """ This method will eventually parse a list of lat/long coordinates and charger information to 
            create the route object. 
        """ 
        name = route[0]   
        stops = route[1]
        tripTime = route[2]
        battery = route[3]

        # Add the starting location and lat/long points. 
        trip = [Start()]

        # For each intermediate charger, add it's information, engery expended to reach the location, and the time to reach the location. 
        for stop in range(1, len(stops) - 1):
            trip.append(Charger(stops[stop][0], stops[stop][1]))

        # Append information about the destination. 
        trip.append(Destination(stops[-1][0], stops[-1][1], stops[-1][2]))

        # Return the trip object. 
        return Trip(name, trip, tripTime, battery)

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