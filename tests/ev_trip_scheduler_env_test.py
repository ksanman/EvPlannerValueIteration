import unittest
from context import Start, Charger, Destination, NissanLeafBattery, EvTripScheduleEnvironment, AddressInfo, Rewards


class EvTripScheduleEnvironmentTest(unittest.TestCase):
    def setUp(self):
        route = [Start("Start", AddressInfo()), Charger(-1,1,1,"Charger",AddressInfo(), 10), Destination(-1,1, 1, "Destination", AddressInfo(),True,10)]
        battery = NissanLeafBattery(3)
        self.env = EvTripScheduleEnvironment(route, 3, battery, Rewards())

    def testEncode(self):
        state = (1,1,1)
        index = 21
        testIndex = self.env.Encode(state[0], state[1], state[2])
        self.assertEqual(index, testIndex)

    def testDecode(self):
        state = (1,1,1)
        index = 21
        stop, time, battery = self.env.Decode(index)
        testState = (stop, time, battery)
        self.assertEqual(state, testState)

if __name__ == '__main__':
    unittest.main(exit=False)