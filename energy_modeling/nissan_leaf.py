from vehicle import Vehicle

class NissanLeaf(Vehicle):
    Mass = 1521
    FrontalArea = 2.3316
    DragCoefficient = 0.28
    DrivelineEfficiency = .92
    MotorEfficiency = .91

    def __init__(self):
        super(NissanLeaf, self).__init__(self.Mass, self.FrontalArea,self.DragCoefficient, self.DrivelineEfficiency, self.MotorEfficiency)