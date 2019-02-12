import unittest

from ev_trip_scheduler_env import EvTripScheduleEnvironment


class EvTripScheduleEnvironmentTest(unittest.TestCase):
    def testEncode(self):
        env = EvTripScheduleEnvironment(3, 3, 3, True)
        state = (1,1,1)
        index = 16
        testIndex = env.Encode(state[0], state[1], state[2])
        self.assertEqual(index, testIndex)

    def testDecode(self):
        env = EvTripScheduleEnvironment(3, 3, 3, True)
        state = (1,1,1)
        index = 16
        stop, time, battery = env.Decode(index)
        testState = (stop, time, battery)
        self.assertEqual(state, testState)

if __name__ == '__main__':
    unittest.main(exit=False)