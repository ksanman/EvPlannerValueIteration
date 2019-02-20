from ..utility import ConvertFromTimeBlockToHours

class Battery(object):
    def __init__(self, capacity):
        """The base class for a ev car battery

            Keyword arguments:

            capacity -- The capacity of the battery. 
        """
        self.Capacity = capacity