import unittest
from context import Start, Charger, Destination, LinearSimpleBattery, EvTripScheduleEnvironment, AddressInfo, Rewards


class Test_EvTripScheduleEnvironment(unittest.TestCase):
    def setUp(self):
        route = [Start("Start", AddressInfo()), Charger(-1,1,1,"Charger",AddressInfo(), 0, 10), Destination(-1,1, 1, "Destination", AddressInfo(),True,0, 10)]
        battery = LinearSimpleBattery(3)
        self.env = EvTripScheduleEnvironment(route, 3, battery, Rewards())

    def test_Encode(self):
        state = (1,1,1)
        index = 21
        testIndex = self.env.Encode(*state)
        self.assertEqual(index, testIndex)

    def test_Decode(self):
        state = (1,1,1)
        index = 21
        stop, time, battery = self.env.Decode(index)
        testState = (stop, time, battery)
        self.assertEqual(state, testState)

if __name__ == '__main__':
    unittest.main(exit=False)