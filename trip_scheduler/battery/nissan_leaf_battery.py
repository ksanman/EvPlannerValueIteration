from battery import Battery
from ..utility import RoundHalfUpToInt, ConvertFromTimeBlockToHours

class NissanLeafBattery(Battery):
    kWhPkm = 4.5 #khw/km
    
    def __init__(self, capacity):
        """ Models the battery of a Nissan Leaf
        """
        super(NissanLeafBattery, self).__init__(capacity)

    def Discharge(self, time, distance):
        """ Calculates the discharge rate of the battery. 
            
            Keyword arguments:

            time -- The duration of the discharge. 
        """
        
        if type(time) != int:
            raise Exception("Time must be represented as an integer value!")

        batteryConsumed = distance / self.kWhPkm
        return -batteryConsumed

    def Charge(self, time, load):
        """ Calculates the Charge in a battery after chargeing for a period of time

            Formula:
            P = load power divided by 1000 = U (voltage) * I (Amperage) / 1000 = Load in KW
            c = power generated in kw
            t = time (in hours)

            c = P * t

            Keyword arguments:

            time -- The duration of charging.
            load -- The load the charger outputs to the battery. 
        """

        if type(time) != int:
            raise Exception("Time must be represented as an integer value!")

        P = load
        t = ConvertFromTimeBlockToHours(time)
        c = RoundHalfUpToInt(t * P)
        return c