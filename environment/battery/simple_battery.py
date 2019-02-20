from battery import Battery

class SimpleBattery(Battery):
    def __init__(self, capacity):
        """Models a simple ev battery
        """
        super(SimpleBattery, self).__init__(capacity)

    def Discharge(self, time):
        """ Calculates the discharge rate of the battery. 
            
            Keyword arguments:

            time -- The duration of the discharge. 
        """
        
        if type(time) != int:
            raise Exception("Time must be represented as an integer value!")

        # For every time block, decrement 1 from the battery charge. 
        currentCharge = 0

        for _ in range(time):
            currentCharge += 1
        
        return -currentCharge