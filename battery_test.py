from battery import Battery
import unittest

class TestBattery(unittest.TestCase):
    def setUp(self):
        self.Battery = Battery(10, 360)

    def testDischarge(self):
        time = 1
        actualCharge = 4
        testCharge = self.Battery.Discharge(time)
        self.assertEqual(testCharge, actualCharge)

        time = 5
        actualCharge = 0
        testCharge = self.Battery.Discharge(time)
        self.assertEqual(testCharge, actualCharge)

    def testCharge(self):
        time = 1
        chargerCurrent = 13.3
        actualCharge = 1
        testCharge = self.Battery.Charge(time, chargerCurrent)
        self.assertEqual(actualCharge, testCharge)

if __name__ == '__main__':
    unittest.main(exit=False)