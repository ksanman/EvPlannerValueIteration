from context import LinearSimpleBattery, RealisticSimpleBattery, NissanLeafBattery
import unittest

class Test_Battery(unittest.TestCase):
    def setUp(self):
        self.LinearBattery = LinearSimpleBattery(10)
        self.RealisticBattery = RealisticSimpleBattery(10)
        self.NissanLeafBattery = NissanLeafBattery(30)

    def test_SimpleDischarge(self):
        time = 1
        actualCharge = -1
        testCharge = self.LinearBattery.Discharge(time, 0)
        self.assertEqual(testCharge, actualCharge)

        time = 5
        actualCharge = -5
        testCharge = self.LinearBattery.Discharge(time, 0)
        self.assertEqual(testCharge, actualCharge)

    def test_SimpleCharge(self):
        time = 1
        chargerCurrent = 100
        chargerVoltage = 400
        load = (chargerCurrent * chargerVoltage) / 1000
        actualCharge = 1
        testCharge = self.LinearBattery.Charge(time, load)
        self.assertEqual(actualCharge, testCharge)

    def test_RealisticSimpleDischarge(self):
        time = 1
        actualCharge = -1
        testCharge = self.RealisticBattery.Discharge(time, 0)
        self.assertEqual(testCharge, actualCharge)

        time = 5
        actualCharge = -5
        testCharge = self.RealisticBattery.Discharge(time, 0)
        self.assertEqual(testCharge, actualCharge)

    def test_RealisticSimpleCharge(self):
        time = 1
        chargerCurrent = 100
        chargerVoltage = 400
        load = (chargerCurrent * chargerVoltage) / 1000
        actualCharge = 10
        testCharge = self.RealisticBattery.Charge(time, load)
        self.assertEqual(actualCharge, testCharge)

    def test_NissanLeafCharge(self):
        time = 1
        chargerCurrent = 100
        chargerVoltage = 400
        load = (chargerCurrent * chargerVoltage) / 1000
        actualCharge = 10
        testCharge = self.NissanLeafBattery.Charge(time, load)
        self.assertEqual(actualCharge, testCharge)

    def test_NissanLeafDischarge(self):
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