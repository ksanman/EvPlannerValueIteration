""" Contains the reward functions used to compute the instant and terminal rewards for an EV Trip Scheduler. 

"""

class Rewards:
    def ComputeTimeReward(self, currentTime, expectedTime):
        """ Computes a reward for a given time step. 
            The reward is negative if the current time step is past the expected time. 
            The reward is positive if the current time step is before the expected time. 

            Keyword arguments:

            currentTime -- The current timestep
            expectedTime -- The expect time to complete the trip. 
        """
        return 1 if currentTime < expectedTime else -1

    def ComputeRewardForDestinationWithoutCharger(self, currentBatteryCharge, batteryCapacity):
        """ Computes the reward given the current battery charge for a Destination without a charger. 
            The reward is 0 if the battery charge is greater than 20% the capacity. 
            The reward is negative if the battery charge is less than 20% the capacity. 

            Keyword arguments:

            currentBatteryCharge -- The current charge level in the battery. 
            batteryCapacity -- The capacity of the battery in KWH. 
        """
        return 0 if currentBatteryCharge > batteryCapacity * .20 else -1 

    def ComputeBatteryRewardForDriving(self, currentBatteryCharge, batteryCapacity):
        """ Computes the reward given the current battery charge after a driving action. 
            The reward is 0 if the battery charge is greater than 10% the capacity. 
            The reward is negative if the battery charge is less than 10% the capacity. 

            Keyword arguments:

            currentBatteryCharge -- The current charge level in the battery. 
            batteryCapacity -- The capacity of the battery in KWH. 
        """
        return 0 if currentBatteryCharge > batteryCapacity * .10 else -1

    def ComputeBatteryRewardForCharging(self, currentBatteryCharge, batteryCapacity):
        """ Computes the reward given the current battery charge after a charging action. 
            The reward is 0 if the battery charge is less than 80% the capacity. 
            The reward is negative if the battery charge is greater than 80% the capacity. 

            Keyword arguments:

            currentBatteryCharge -- The current charge level in the battery. 
            batteryCapacity -- The capacity of the battery in KWH. 
        """
        return -1 if currentBatteryCharge > batteryCapacity * .80 else 0