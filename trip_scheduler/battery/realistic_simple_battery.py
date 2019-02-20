from battery import Battery
from ..utility import ConvertFromTimeBlockToHours, RoundHalfUpToInt

class RealisticSimpleBattery(Battery):
    def __init__(self, capacity):
        """Models a simple ev battery
        """
        super(RealisticSimpleBattery, self).__init__(capacity)

    def Discharge(self, time, distance):
        """ Calculates the discharge rate of the battery. 
            
            Keyword arguments:

            time -- The duration of the discharge. 
            distance -- The distance traveled.
        """
        
        if type(time) != int:
            raise Exception("Time must be represented as an integer value!")

        # For every time block, decrement 1 from the battery charge. 
        currentCharge = 0

        for _ in range(time):
            currentCharge += 1
        
        return -currentCharge

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