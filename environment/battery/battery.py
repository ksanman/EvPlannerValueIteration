class Battery(object):
    def __init__(self, capacity):
        """The base class for a ev car battery

            Keyword arguments:

            capacity -- The capacity of the battery. 
        """
        self.Capacity = capacity

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
        t = self.ConvertToHours(time)
        c = (t * P)
        return c

    def ConvertToHours(self, timeBlock):
        """ Converts a 15 minute time block to hours

            Keyword arguments:

            timeBlock -- A block of time. Each interger increment is 15 minutes. 
        """
        hours = (timeBlock * 15) / 60.0
        return hours