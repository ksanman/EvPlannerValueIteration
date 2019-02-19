"""
File contains definitions for the different types of Stops that can be encountered during the trip
"""

class Stop(object):
    def __init__(self, expendedEnergy, tripTime, distance, name, addressInfo):
        """ Base representation of a stop along a vehicles route. 

            Keyword arguments:

            expendedEnergy -- The energy required to travel from the previous stop to the current stop. 
            tripTime -- The duration of the trip from the previous stop to the current stop. 
            distance -- The distance from the previous stop to the current stop
            name -- The name of the current stop (Address)
            addressInfo -- Address information about the location. 
        """

        self.ExpendedEnergy = expendedEnergy
        self.TripTime = tripTime
        self.Distance = distance
        self.Name = name
        self.AddressInfo = addressInfo

class Start(Stop):
    def __init__(self, name, addressInfo):
        """ Represents the starting point of the route. 
            There are no properties for a starting point as there is no previous stop. 

            Keyword arguments:

            name -- The name of the current stop (Address)
            addressInfo -- Address information about the location. 
        """
        super(Start, self).__init__(0, 0, 0, name, addressInfo)

class Charger(Stop):
    def __init__(self, expendedEnergy, tripTime, distance, name, addressInfo, load):
        """ Represents a charging station along a route. 

            Keyword arguments:

            expendedEnergy -- The energy required to travel from the previous stop to the current stop. 
            tripTime -- The duration of the trip from the previous stop to the current stop. 
            distance -- The distance from the previous stop to the current stop
            name -- The name of the current stop (Address)
            voltage -- The voltage of the charging station
            addressInfo -- Address information about the location.
            current -- The current (in amps) that the charging station delivers. 
        """
        self.Load = load
        super(Charger, self).__init__(expendedEnergy, tripTime, distance, name, addressInfo)

class Destination(Stop):
    def __init__(self, expendedEnergy, tripTime, distance, name, addressInfo, hasCharger, load=0):
        """ Represents the Destination of the route. 

            Keyword arguments:

            expendedEnergy -- The energy required to travel from the previous stop to the current stop. 
            tripTime -- The duration of the trip from the previous stop to the current stop.
            distance -- The distance from the previous stop to the current stop
            name -- The name of the current stop (Address)
            voltage -- The voltage of the charging station
            current -- The current (in amps) that the charging station delivers. 
            addressInfo -- Address information about the location.
            hasCharger -- Indicates whether or not the destination has a charging station or not.  
        """
        self.Load = load
        self.HasCharger = hasCharger
        super(Destination, self).__init__(expendedEnergy, tripTime, distance, name, addressInfo)


