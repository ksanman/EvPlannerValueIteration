from battery import Battery

class NissanLeafBattery(Battery):
    def __init__(self, capacity):
        """ Models the battery of a Nissan Leaf
        """
        super(NissanLeafBattery, self).__init__(capacity)

    def Discharge(self, time):
        """ Calculates the discharge rate of the battery. 
            
            Keyword arguments:

            time -- The duration of the discharge. 
        """
        
        if type(time) != int:
            raise Exception("Time must be represented as an integer value!")

        raise Exception('Discharge not implemented for Nissan Leaf Battery!') 