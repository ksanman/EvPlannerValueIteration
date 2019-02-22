import unittest
from context import NissanLeaf, RoadConditions, EnergyConsumptionModel

class Test_EnergyConsumptionModel(unittest.TestCase):
    def setUp(self):
        self.NissanLeaf = NissanLeaf()
        self.RoadConditions = RoadConditions(1.75, 0.0328, 4.575)
        self.EnergyConsumptionModel = EnergyConsumptionModel()

    def test_PowerAtWheelsAtOneTimeStep(self):
        power = self.EnergyConsumptionModel.ComputePowerToWheels(self.NissanLeaf, 0.0, 29.1, 0.0, self.RoadConditions)
        expectedPower = 14058.609040059986
        self.assertEqual(power, expectedPower)

if __name__ == '__main__':
    unittest.main(exit=False)