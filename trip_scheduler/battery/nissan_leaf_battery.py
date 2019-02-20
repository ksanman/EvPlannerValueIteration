from battery import Battery
from ..utility import RoundHalfUpToInt, ConvertFromTimeBlockToHours

class NissanLeafBattery(Battery):
    kWhPkm = 0.212
    
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

        batteryConsumed = distance * self.kWhPkm
        return -batteryConsumed