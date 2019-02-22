class Vehicle(object):
    def __init__(self, mass, frontalArea, dragCoefficient, drivelineEfficiency, motorEfficiency):
        self.Mass = mass
        self.FrontalArea = frontalArea
        self.DragCoefficient = dragCoefficient
        self.DrivelineEfficiency = drivelineEfficiency
        self.MotorEfficiency = motorEfficiency