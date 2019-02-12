import numpy as np
from matplotlib.pyplot import plot

from ev_trip_scheduler_env import EvTripScheduleEnvironment


class ValueIterationAgent:
    def __init__(self, environment):
        self.Environment = environment
        self.V = np.zeros(self.Environment.NumberOfStates)
        self.Policy = np.zeros(self.Environment.NumberOfStates)
        self.Discount = 1.0

    def PerformValueIteration(self):
        iteration = 0
        while True:
            delta = 0
            v_copy = self.V.copy()
            iteration += 1

            for state in range(self.Environment.NumberOfStates):
                action_reward_values = []
                for action in self.Environment.GetActionSpaceForState(state):
                    action_reward_values.append(self.Environment.P[state][action][0][2] + self.Discount * self.V[self.Environment.P[state][action][0][1]])
                
                if action_reward_values == []:
                    continue

                self.V[state] = np.argmax(action_reward_values)

            delta = np.sum(np.fabs(v_copy - self.V))
            if(delta <= 0.1):
                break

    def PrintVTable(self):
        stops = self.Environment.Stops
        maxTime = self.Environment.MaxTime
        maxBattery = self.Environment.MaxBattery
        v3d = self.V.reshape((stops,maxTime,maxBattery)).transpose()
        state = 0
        for k in range(maxBattery):
            for j in range(maxTime):
                for i in range(stops):
                    v3d[i,j,k] = self.V[state]
                    state += 1

        print '\n V Table: \n'
        print v3d

    def FindOptimalPolicy(self):
        for state in range(self.Environment.NumberOfStates):
            action_values = []
            for action in self.Environment.GetActionSpaceForState(state):
                action_values.append(self.Environment.P[state][action][0][2] + self.V[self.Environment.P[state][action][0][1]])
            
            # If the action space is empty, continue
            if action_values == []:
                continue

            self.Policy[state] = np.argmax(action_values)
    
    def PrintPolicy(self):
        stops = self.Environment.Stops
        maxTime = self.Environment.MaxTime
        maxBattery = self.Environment.MaxBattery
        p3d = self.Policy.reshape((stops,maxTime,maxBattery)).transpose()
        state = 0
        for k in range(maxBattery):
            for j in range(maxTime):
                for i in range(stops):
                    p3d[i,j,k] = self.Policy[state]
                    state += 1

        print '\n V Table: \n'
        print p3d

    def EvaluatePolicy(self, numberOfTestRuns, randomState):
        average_reward = 0
        self.TestRunInfo = []

        for testRun in range(numberOfTestRuns):
            print 'Test Run #: ', testRun
            runInfo = {testRun: {}}

            state = self.Environment.Reset(randomState)
            total_reward = 0
            step_index = 0
            self.ChargingPoints = {}

            while True:
                # Get the optimal action. 
                actionToTake = int(self.Policy[state])
                runInfo[testRun].update({step_index: {"Start State": state, "Action": actionToTake}})
                # Act.  
                state, reward, done, _ = self.Environment.Step(actionToTake)

                runInfo[testRun][step_index].update({"End State": state, "Reward": reward, "Is Terminated": done})
                

                # if the action is charging, add the waypoint to a list of coordinates to display once the test
                # is finished. 
                if actionToTake == 1:
                    stop, _, _ = self.Environment.Decode(state)
                    if stop not in self.ChargingPoints:
                        self.ChargingPoints[stop] = 1
                    else:
                        self.ChargingPoints[stop] += 1
                
                total_reward += reward

                runInfo[testRun][step_index].update({"Step Total Reward": total_reward})

                step_index += 1
                

                if done:
                    break
            #Print the trip stats. 
            #runInfo[testRun].update({"Average Reward": average_reward})
            average_reward += total_reward
            self.PrintEvaluation(state, total_reward)
            print 'Average reward: ', average_reward/(testRun + 1), '\n\n'
        
            self.TestRunInfo.append(runInfo)

        print 'Total average reward: ', average_reward/numberOfTestRuns

    def PrintEvaluation(self, state, reward):
        stop, time, battery = self.Environment.Decode(state)
        print 'Battery level: ', battery
        print 'Trip time: ', time * 15, ' minutes'
        for _,p in self.ChargingPoints.items():
            w = stop
            t = p*15
            s = 'Stop at {0} for {1} minutes.'.format(w, t)
            print(s)

    def DisplayEvaluationGraphs(self):
        print self.TestRunInfo

        batteryPairs = []

        for run in self.TestRunInfo:
            for step in run[0]:
                startState = run[0][step]["Start State"]
                endState = run[0][step]["End State"]
                startStop, startTime, startBattery = self.Environment.Decode(startState)
                endStop, endTime, endBattery = self.Environment.Decode(endState)
                batteryPairs.append([startBattery, endBattery])


        #plot Here
