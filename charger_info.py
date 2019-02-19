class Point(object):
    def __init__(self, name, latitude, longitude):
        self.Name = name
        self.Latitude = latitude
        self.Longitude = longitude

class ChargerPoint(Point):
    def __init__(self, id, name, latitude, longitude, voltage, current):
        self.Current = current
        self.Voltage = voltage
        super(ChargerPoint, self).__init__(name, latitude, longitude)