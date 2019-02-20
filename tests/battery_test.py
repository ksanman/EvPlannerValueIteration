from context import SimpleBattery, NissanLeafBattery
import unittest

class TestBattery(unittest.TestCase):
    def setUp(self):
        self.Battery = SimpleBattery(10)
        self.NissanLeafBattery = NissanLeafBattery(30)

    def testDischarge(self):
        time = 1
        actualCharge = -1
        testCharge = self.Battery.Discharge(time, 0)
        self.assertEqual(testCharge, actualCharge)

        time = 5
        actualCharge = -5
        testCharge = self.Battery.Discharge(time, 0)
        self.assertEqual(testCharge, actualCharge)

    def testCharge(self):
        time = 1
        chargerCurrent = 100
        chargerVoltage = 400
        load = (chargerCurrent * chargerVoltage) / 1000
        actualCharge = 10
        testCharge = self.Battery.Charge(time, load)
        self.assertEqual(actualCharge, testCharge)

    def testNissanLeafDischarge(self):
        time = 2
        distance = 30
        actualCharge = -6.359999999999999
        testCharge = self.NissanLeafBattery.Discharge(time, distance)
        self.assertEqual(testCharge, actualCharge)

        time = 4
        distance = 0
        actualCharge = 0
        testCharge = self.NissanLeafBattery.Discharge(time, distance)
        self.assertEqual(testCharge, actualCharge)

if __name__ == '__main__':
    unittest.main(exit=False)