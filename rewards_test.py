from rewards import Rewards
import unittest

class Test_Rewards(unittest.TestCase):
    def setUp(self):
        self.RewardFunctions = Rewards()
    
    def test_ComputeTimeReward(self):
        testTimes = [
            [0,4,4],
            [1,4,3],
            [5,4,-1]
        ]

        for time, expected, reward in testTimes:
            actualReward = self.RewardFunctions.ComputeTimeReward(time, expected)
            self.assertEqual(reward, actualReward)

    def test_ComputeRewardForDestinationWithoutCharger(self):
        testTimes = [
            [0,10,-100],
            [3,10,0],
            [10,10,0]
        ]

        for battery, capacity, reward in testTimes:
            actualReward = self.RewardFunctions.ComputeRewardForDestinationWithoutCharger(battery, capacity)
            self.assertEqual(reward, actualReward)

    def test_ComputeBatteryRewardForDriving(self):
        testTimes = [
            [0,10,-10],
            [2,10,0],
            [10,10,0]
        ]

        for battery, capacity, reward in testTimes:
            actualReward = self.RewardFunctions.ComputeBatteryRewardForDriving(battery, capacity)
            self.assertEqual(reward, actualReward)

    def test_ComputeBatteryRewardForCharging(self):
        testTimes = [
            [1,10, 1, -0.13],
            [3,10,3, -0.39],
            [9,10,1,-100]
        ]

        for battery, capacity, power, reward in testTimes:
            actualReward = self.RewardFunctions.ComputeBatteryRewardForCharging(battery, capacity, power)
            self.assertEqual(reward, actualReward)

if __name__ == '__main__':
    unittest.main(exit=False)