"""
File contains definitions for the different types of Stops that can be encountered during the trip
"""

class Stop(object):
    def __init__(self, expendedEnergy, tripTime, distance, name):
        """ Base representation of a stop along a vehicles route. 

            Keyword arguments:

            expendedEnergy -- The energy required to travel from the previous stop to the current stop. 
            tripTime -- The duration of the trip from the previous stop to the current stop. 
        """

        self.ExpendedEnergy = expendedEnergy
        self.TripTime = tripTime
        self.Distance = distance
        self.Name = name

class Start(Stop):
    def __init__(self, name):
        """ Represents the starting point of the route. 
        There are no properties for a starting point as there is no previous stop. 
        """
        super(Start, self).__init__(0, 0, 0, name)

class Charger(Stop):
    def __init__(self, expendedEnergy, tripTime, distance, name, current):
        """ Represents a charging station along a route. 

            Keyword arguments:

            expendedEnergy -- The energy required to travel from the previous stop to the current stop. 
            tripTime -- The duration of the trip from the previous stop to the current stop. 
        """
        self.Current = current
        super(Charger, self).__init__(expendedEnergy, tripTime, distance, name)

class Destination(Stop):
    def __init__(self, expendedEnergy, tripTime, distance, name, hasCharger):
        """ Represents the Destination of the route. 

            Keyword arguments:

            expendedEnergy -- The energy required to travel from the previous stop to the current stop. 
            tripTime -- The duration of the trip from the previous stop to the current stop.
            hasCharger -- Indicates whether or not the destination has a charging station or not.  
        """
        self.HasCharger = hasCharger
        super(Destination, self).__init__(expendedEnergy, tripTime, distance, name)


