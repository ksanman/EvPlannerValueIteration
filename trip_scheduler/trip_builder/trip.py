class Trip:
    """ An object used to hold information about a particular trip. 
    """
    def __init__(self, name, route, polyline, tripTime, battery):
        self.Name = name
        self.Route = route
        self.TripTime = tripTime
        self.Battery = battery
        self.Polyline = polyline
