class Battery(object):
    def __init__(self, capacity):
        """The base class for a ev car battery

            Keyword arguments:

            capacity -- The capacity of the battery. 
        """
        self.Capacity = capacity

    def Discharge(self, currentCharge, time):
        """ Calculates the discharge rate of the battery. 
            
            Keyword arguments:

            currentCharge -- The current charge in the battery
            time -- The duration of the discharge. 
        """
        
        if type(time) != int:
            raise Exception("Time must be represented as an integer value!")

        # For every time block, decrement 1 from the battery charge. 
        for _ in range(time):
            currentCharge -= 1
        
        return currentCharge


    def Charge(self, currentCharge, time):
        """ Calculates the Charge in a battery after chargeing for a period of time

            Keyword arguments:

            currentCharge -- The current charge in the battery
            time -- The duration of charging.
        """

        if type(time) != int:
            raise Exception("Time must be represented as an integer value!")

        # For every time block, increment 1 from the battery charge. 
        for _ in range(time):
            currentCharge += 1
        
        return currentCharge


class NissanLeafBattery(Battery):
    def __init__(self, capacity):
        """ Models the battery of a Nissan Leaf
        """
        super(NissanLeafBattery, self).__init__(capacity)
