from decimal import Decimal, ROUND_HALF_UP

class Battery(object):
    KwhToWattHourConversionFactor = 1000
    LionBatteryEfficiency = .90

    def __init__(self, capacity, systemVoltage):
        """The base class for a ev car battery

            Keyword arguments:

            capacity -- The capacity of the battery. 
        """
        self.Capacity = capacity
        self.SystemVoltage = systemVoltage

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


    def Charge(self, currentCharge, time, chargerCurrent):
        """ Calculates the Charge in a battery after chargeing for a period of time

            Keyword arguments:

            currentCharge -- The current charge in the battery
            time -- The duration of charging.
        """

        if type(time) != int:
            raise Exception("Time must be represented as an integer value!")

        # For every time block, increment 1 from the battery charge. 
        hours = self.ConvertToHours(time)
        charge = ( hours * self.LionBatteryEfficiency * chargerCurrent)
        kwh = int(Decimal(self.AhToKwh(charge)).quantize(Decimal('0'), rounding=ROUND_HALF_UP))
        return kwh

    def ConvertToHours(self, timeBlock):
        """ Converts a 15 minute time block to hours

            Keyword arguments:

            timeBlock -- A block of time. Each interger increment is 15 minutes. 
        """
        hours = (timeBlock * 15) / 60.0
        return hours

    def AhToKwh(self, ah):
        """
        Converts AH to KWH based on the system voltage.
        """
        return ((ah * self.SystemVoltage) / self.KwhToWattHourConversionFactor)

class NissanLeafBattery(Battery):
    def __init__(self, capacity):
        """ Models the battery of a Nissan Leaf
        """
        nissanLeafSystemVoltage = 360
        super(NissanLeafBattery, self).__init__(capacity, nissanLeafSystemVoltage)
