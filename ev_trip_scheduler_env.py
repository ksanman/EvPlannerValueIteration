import hashlib
import random as _random
from decimal import ROUND_HALF_UP, Decimal

import numpy as np

from action import (ActionSpace, ChargerActionSpace, DestinationActionSpace,
                    StartActionSpace)
from randomizer import Randomizer
from rewards import Rewards


class EvTripScheduleEnvironment:
    """ Represents the Trip Schedule. The schedule is a list of possible charging stations along a route, the car battery, and the time to make the trip. 
    The maximum time allocated to make the trip is 20% of the expected time.
    """
    def __init__(self, route, expectedTripTime, battery):
        # Define the environment variables here. 
        self.Route = route
        self.Stops = len(route) 

        self.ExpectedTime = expectedTripTime
        self.MaxTime = self.ExpectedTime + int(Decimal(self.ExpectedTime * .20).quantize(Decimal('0'), rounding=ROUND_HALF_UP))

        self.Battery = battery
        self.MaxBattery = battery.Capacity + 1
        
        self.IsDestinationCharger = route[-1].HasCharger

        # Set the action space
        self.ActionSpace = self.InitializeActionSpace()

        print "\n\n Environment: \n\n Number of Stops: {0}\n Battery Capacity: {1}\n Expected Trip Time: {2}\n Max Time: {3} \n Destination Has a Charger: {4}\n".format(self.Stops, battery.Capacity, self.ExpectedTime, self.MaxTime, self.IsDestinationCharger)

        # Construct the environment here:
        self.NumberOfStates = self.Stops * self.MaxTime * self.MaxBattery

        print " Number of states: {0}\n Action Space: {1}".format(self.NumberOfStates, len(self.ActionSpace))

        # Array that contains the intial state distribution quantities
        self.InitialStateDistribution = np.zeros(self.NumberOfStates)

        # P are the transtions from state s, with action a, to state s'.
        # It contains the probability of event happeneing, s', the reward, and if s' is terminal. 
        # There are at most 2 actions for each state. 
        self.P = {state: {action: [] for action in range(2)} for state in range(self.NumberOfStates)}
        self.RewardFunctions = Rewards()
        self.InitializeEnvironment()
    
    def InitializeEnvironment(self):
        for stop in range(self.Stops):
            for time in range(self.MaxTime):
                for battery in range(self.MaxBattery):
                    state = int(self.Encode(stop, time, battery))

                    if stop == 0:
                        self.InitialStateDistribution[state] += 1
                    
                    actionSpace = self.ActionSpace[stop][time][battery]

                    for action in actionSpace:
                        self.PopulatePTable(state, stop, time, battery, action)

        self.InitialStateDistribution /= self.InitialStateDistribution.sum()
        self.Seed()
        self.Reset()

    def PopulatePTable(self, state,  stop, time, battery, action):
        reward = 0.0
        done = False

        # if the action is driving
        if action == ActionSpace.Drive:
            nextStop = min(stop + 1, self.Stops - 1)
            location = self.Route[nextStop]

            nextTime = min(time + location.TripTime, self.MaxTime - 1)
            nextBattery = max(battery + location.ExpendedEnergy, 0)

            # Set the time reward
            reward += self.ComputeReward((nextTime, self.MaxTime), self.RewardFunctions.ComputeTimeReward)

            # If the new state is the terminal state
            if nextStop == self.Stops - 1:
                # If there is not a charger at the terminal state, set a reward for having a battery over 20%.
                if not self.IsDestinationCharger:
                    reward += self.ComputeReward((nextBattery, self.MaxBattery), self.RewardFunctions.ComputeRewardForDestinationWithoutCharger)
            else:
                # Set the reward for all other driving states
                reward += self.ComputeReward((nextBattery, self.MaxBattery), self.RewardFunctions.ComputeBatteryRewardForDriving)

        # Otherwise the action is charging
        elif action == ActionSpace.Charge:
            nextStop = stop
            nextTime = min(time + 1, self.MaxTime - 1)
            nextBattery = min(self.Battery.Charge(battery, nextTime - time, 13.3), self.MaxBattery - 1)

            # Set the time reward
            reward += self.ComputeReward((nextTime, self.MaxTime), self.RewardFunctions.ComputeTimeReward)
            # Set the charging reward. The reward is negative for staying too long at a charger and overcharging the car. 
            reward += self.ComputeReward((nextBattery, self.MaxBattery, nextBattery - battery), self.RewardFunctions.ComputeBatteryRewardForCharging)

        # If there are no actions, return
        elif action == None:
            return

        # If the vehicle is at the last stop, the time limit is exceeded, or the battery ran out and the car is not charging then done it true. 
        if nextStop == self.Stops - 1 \
            or nextTime == self.MaxTime - 1\
                    or (nextBattery == 0 and action is not 1):
            done = True

        newState = int(self.Encode(nextStop, nextTime, nextBattery))
        self.P[state][action].append((1.0, newState, reward, done))

    def InitializeActionSpace(self):
        actionSpace = [[[ None for _ in range(self.MaxBattery)] for _ in range(self.MaxTime)] for _ in range(self.Stops)]

        for stop in range(self.Stops):
            for time in range(self.MaxTime):
                for battery in range(self.MaxBattery):
                    if stop == 0:
                        # If the state is at the start location, the only available action is driving. 
                        actionSpace[stop][time][battery] = StartActionSpace().Actions 
                    elif stop == self.Stops - 1:
                        # If the state is at the destination, the action space is empty. 
                        actionSpace[stop][time][battery] = DestinationActionSpace().Actions
                    else:
                        # Other wise, the action space contains driving or charging. 
                        actionSpace[stop][time][battery] = ChargerActionSpace().Actions

        return actionSpace

    def GetActionSpaceForState(self, state):
        """ Get the available actions for the selected state. 
        """
        stop, time, battery = self.Decode(state)
        return self.ActionSpace[stop][time][battery]      

    def Encode(self, stop, time, battery):
        i = stop
        i *= self.MaxTime
        i += time
        i *= self.MaxBattery
        i += battery
        return i

    def Decode(self, i):
        out = []
        out.append(i % self.MaxBattery)
        i = i // self.MaxBattery
        out.append(i % self.MaxTime)
        i = i // self.MaxTime
        out.append(i)
        assert 0 <= i < self.Stops
        return reversed(out)

    def Seed(self, seed=None):
        randomizer = Randomizer()
        self.Randomizer, seed = randomizer.intialize(seed)
        return [seed]

    def Reset(self, random=False):
        """ Resets the environment state to an intial state. 
            If the random value is false, then the state at the first stop, first time step, and full battery will be selected. 
        """

        if random:
            self.State = self.SampleFromInitialState(self.InitialStateDistribution)
        else:
            self.State = self.Encode(0,0,self.MaxBattery - 1)
        self.LastAction = None
        return self.State
    
    def SampleFromInitialState(self, probability_array):
        probability_array = np.asarray(probability_array)
        cumsum_probability_array = np.cumsum(probability_array)
        return (cumsum_probability_array > self.Randomizer.rand()).argmax()

    def Step(self, action):
        """ Move the state of the environment forward one time step with the given action. 
        """
        transitions = self.P[self.State][action]
        i = self.SampleFromInitialState([t[0] for t in transitions])
        probability, state, reward, done = transitions[i]
        self.State = state
        self.LastAction = action
        return (state, reward, done, {"prob" : probability})

    def ComputeReward(self, args, rewardFunction):
        return rewardFunction(*args)