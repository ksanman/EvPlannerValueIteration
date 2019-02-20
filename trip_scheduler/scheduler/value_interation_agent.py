import numpy as np
import matplotlib.pyplot as plt
import os
from collections import OrderedDict
from ..utility import RoundHalfUpToInt
from ..environment.ev_trip_scheduler_env import EvTripScheduleEnvironment


class ValueIterationAgent:
    def __init__(self, environment):
        self.Environment = environment
        self.V = np.zeros(self.Environment.NumberOfStates)
        self.Policy = np.zeros(self.Environment.NumberOfStates)
        self.Discount = 1.0

    def PerformValueIteration(self, isShowable=False):
        """ Performs value iteration on the enviroment and populates the v-table. 
        """
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

        if isShowable:                
            self.PrintVTable()

    def PrintVTable(self):
        """ Prints the V Table to the standard output. 
        """
        stops = self.Environment.Stops
        maxTime = self.Environment.MaxTime
        maxBattery = self.Environment.MaxBattery
        v3d = self.V.reshape((stops,maxTime,maxBattery))
        state = 0
        for s in range(stops):
            for t in range(maxTime):
                for b in range(maxBattery):
                    v3d[s,t,b] = self.V[state]
                    state += 1

        print '\n V Table: \n'
        print v3d

    def FindOptimalPolicy(self, isShowable=False):
        """ Finds the optimal policy with the pre-computed V Table. 
        """

        for state in range(self.Environment.NumberOfStates):
            action_values = []
            for action in self.Environment.GetActionSpaceForState(state):
                action_values.append(self.Environment.P[state][action][0][2] + self.V[self.Environment.P[state][action][0][1]])
            
            # If the action space is empty, continue
            if action_values == []:
                continue

            self.Policy[state] = np.argmax(action_values)
        
        if isShowable:
            self.PrintPolicy()
    
    def PrintPolicy(self):
        """Prints the optimal policy table to the standard output. 
        """

        stops = self.Environment.Stops
        maxTime = self.Environment.MaxTime
        maxBattery = self.Environment.MaxBattery
        p3d = self.Policy.reshape((stops,maxTime,maxBattery))
        state = 0
        for s in range(stops):
            for t in range(maxTime):
                for b in range(maxBattery):
                    p3d[s,t,b] = self.Policy[state]
                    state += 1

        print '\n Policy Table: \n'
        print p3d

    def EvaluatePolicy(self, numberOfTestRuns, randomState, isShowable=False):
        """ Evaluates the given policy as a real-time agent. 

            Keyword arguments:
            numberOfTestRuns -- The number of test runs to perform. 
            randomState -- Boolean that determines if the environment should start in a random state or the initial state (Ev car at the Start, 0 time, and fully charges)
            isShowable -- Boolean to determine if the evaluation should print to the standard output as it runs. 
        """
        average_reward = 0
        self.TestRunInfo = {}

        for testRun in range(numberOfTestRuns):
            
            if isShowable:
                print 'Test Run #: ', testRun + 1
            
            runInfo = {testRun: {"Steps": {}}}

            state = self.Environment.Reset(randomState)

            if isShowable:
                print "Stop: {0}, Time: {1}, Battery: {2}".format(*self.Environment.Decode(state))

            runInfo[testRun]["Steps"].update({0: {"State": state, "Action": None, "Reward": 0, "Is Terminated": False, 'Step Total Reward': 0}})
            total_reward = 0
            step_index = 1
            self.ChargingPoints = OrderedDict()

            while True:
                # Get the optimal action. 
                actionToTake = int(self.Policy[state])
                
                # Act.  
                state, reward, done, _ = self.Environment.Step(actionToTake)
                
                if isShowable:
                    print "Stop: {0}, Time: {1}, Battery: {2}".format(*self.Environment.Decode(state))

                runInfo[testRun]["Steps"].update({step_index: {"State": state, "Action": actionToTake, "Reward": reward, "Is Terminated": done}})
                

                # if the action is charging, add the waypoint to a list of coordinates to display once the test
                # is finished. 
                if actionToTake == 1:
                    stop, _, _ = self.Environment.Decode(state)
                    if stop not in self.ChargingPoints:
                        self.ChargingPoints[stop] = 1
                    else:
                        self.ChargingPoints[stop] += 1
                
                total_reward += reward

                runInfo[testRun]["Steps"][step_index].update({"Step Total Reward": total_reward})

                step_index += 1

                if done:
                    break
            #Print the trip stats. 
            runInfo[testRun].update({"Average Reward": average_reward})
            average_reward += total_reward

            self.BuildSchedule(state)

            if isShowable:
                self.PrintEvaluation(state, total_reward)
                print 'Average reward: ', average_reward/(testRun + 1), '\n\n'
        
            self.TestRunInfo.update(runInfo)
        if isShowable:
            print 'Total average reward: ', average_reward/numberOfTestRuns

    def PrintEvaluation(self, state, reward):
        """ Prints the evaluation of each test run to the standard output. 
        """
        stop, time, battery = self.Environment.Decode(state)
        print 'Battery level: ', battery
        print 'Trip time: ', time * 15, ' minutes'
        if stop != self.Environment.Stops - 1:
            print 'Trip Failed at stop: {0}'.format(stop)
        
        for w ,t in self.ChargingPoints.items():
            s = 'Stop at {0} for {1} minutes ({2} time steps).'.format(self.Environment.Route[w].Name, t*15, t)
            print(s)

    def BuildSchedule(self, state):
        """ After the policy is evaluated, an optimal schedule is built.
        """
        stop, time, battery = self.Environment.Decode(state)
        if stop != self.Environment.Stops - 1:
            self.Schedule = {"Failed": "Trip Failed at stop {0} after {1} minutes ({2} time steps).".format(stop, time*15, time)}
        else:
            self.Schedule = {"Success": {"Trip Time": '{0} Minutes ({1} time steps)'.format(time*15, time), "Battery": battery, "Charging Stops": []}}
            for w, t in self.ChargingPoints.items():
                s = 'Stop at {0} for {1} minutes ({2} time steps).'.format(self.Environment.Route[w].Name, t*15, t)
                self.Schedule["Success"]["Charging Stops"].append(s)

    def GetSchedule(self):
        """ Return a computed schedule to the user. 
        """
        if self.Schedule is None:
             raise Exception("No Schedule Found!")
        return self.Schedule 

    def DisplayEvaluationGraphs(self, routeName = ""):
        """ Display diagnostic graphs to see if the algorithm is working as expected. 

            Keyword arguments:

            routeName -- The name of the current route to append to figures. 
        """
        batteryInfo = []
        batteryDistance = []
        timeDistance = []

        for run in self.TestRunInfo:
            for step in self.TestRunInfo[run]["Steps"]:
                state = self.TestRunInfo[run]["Steps"][step]["State"]
                action = self.TestRunInfo[run]["Steps"][step]["Action"]
                stop, time, battery = self.Environment.Decode(state)
                location = self.Environment.Route[stop]
                batteryInfo.append([battery, time])
                if action == 0:
                    batteryDistance.append([battery, location.Distance])
                    timeDistance.append([time, location.Distance])
                else:
                    # There is no distance while charging. 
                    batteryDistance.append([battery, 0])
                    timeDistance.append([time, 0])


        self.PlotBatteryInfo(batteryInfo, routeName)
        self.PlotBatteryVsTime(batteryDistance, routeName)
        self.PlotTimeVsDistance(timeDistance, routeName)

    def PlotBatteryVsTime(self, batteryDistance, routeName):
        """ Plots the battery level as a funtion of battery level and distance. 
        """
        batteryDistance = np.array(batteryDistance)
        distance = batteryDistance[:, 1]
        battery = batteryDistance[:, 0]

        milage = []
        total = 0
        for d in distance:
            total += d
            milage.append(total)

        #plot Here
        figure, batteryAxes = plt.subplots()
        plt.ylim(ymax=self.Environment.MaxBattery, ymin=0)
        plt.xlim(xmin=0, xmax=max(milage))
        
        batteryAxes.plot(milage, battery)

        yTickSpacing = RoundHalfUpToInt((max(battery) + 1)/10) if max(battery) + 1 > 10 else 1
        plt.yticks(np.arange(0, max(battery) + 1, yTickSpacing))

        xTickSpacing = RoundHalfUpToInt((max(milage) + 1)/10) if max(milage) + 1 > 10 else 1
        plt.xticks(np.arange(0, max(milage) + 1, xTickSpacing))

        labels = batteryAxes.get_xticklabels()
        plt.setp(labels, horizontalalignment='right')
        batteryAxes.set(xlabel='Distance', ylabel='Battery Charge', title=routeName + ': Battery Charge vs Distance')


        if routeName == "":
            plt.show()
        else:
            if not os.path.exists("temp"):
                os.mkdir('temp/')

            figure.savefig('temp/' + routeName + '_BatteryChargeVsDistance.png', dpi=figure.dpi)

    def PlotTimeVsDistance(self, timeDistance, routeName):
        """ Plots the time as a funtion of distance. 
        """ 
        timeDistance = np.array(timeDistance)
        distance = timeDistance[:, 1]
        milage = []
        total = 0
        for d in distance:
            total += d
            milage.append(total)

        time = timeDistance[:, 0]

        #plot Here
        figure, axes = plt.subplots()
       


        # Horizantal Time
        #plt.xlim(xmax=self.Environment.MaxTime, xmin=0)
        #plt.ylim(ymin=0)
        #axes.plot(time, milage)
        # xTickSpacing = int(Decimal((self.Environment.MaxTime + 1)/10).quantize(Decimal('0'), rounding=ROUND_HALF_UP)) if self.Environment.MaxTime + 1 > 10 else 1
        # plt.xticks(np.arange(0, self.Environment.MaxTime + 1, xTickSpacing))
        # yTickSpacing = int(Decimal((max(milage) + 1)/10).quantize(Decimal('0'), rounding=ROUND_HALF_UP)) if max(milage) + 1 > 10 else 1
        # plt.yticks(np.arange(0, max(milage) + 1, yTickSpacing))
        #labels = axes.get_xticklabels()
        #plt.setp(labels, horizontalalignment='right')
        #axes.set(xlabel='Time', ylabel='Distance', title=routeName + ': Distance vs Time')

        #Vertical Time
        plt.ylim(ymax=self.Environment.MaxTime, ymin=0)
        plt.xlim(xmin=0)
        axes.plot(milage, time)
        yTickSpacing = RoundHalfUpToInt(self.Environment.MaxTime) if self.Environment.MaxTime + 1 > 10 else 1
        plt.yticks(np.arange(0, self.Environment.MaxTime + 1, yTickSpacing))
        xTickSpacing = RoundHalfUpToInt((max(milage) + 1)/10) if max(milage) + 1 > 10 else 1
        plt.xticks(np.arange(0, max(milage) + 1, xTickSpacing))

        labels = axes.get_xticklabels()

        plt.setp(labels, horizontalalignment='right')
        axes.set(xlabel='Distance', ylabel='Time', title=routeName + ': Distance vs Time')

        
        if routeName == "":
            plt.show()
        else:
            if not os.path.exists("temp"):
                os.mkdir('temp/')

            figure.savefig('temp/' + routeName + '_TimeVsDistance.png', dpi=figure.dpi)

    def PlotBatteryInfo(self, batteryInfo, routeName):
        """ Plots the battery level as a funtion of battery level and time. 
        """
        batteryInfo = np.array(batteryInfo)
        expectedTime = self.Environment.ExpectedTime

        #plot Here
        figure, batteryAxes = plt.subplots()
        plt.ylim(ymax=self.Environment.MaxBattery, ymin=0)
        plt.xlim(xmax=self.Environment.MaxTime,xmin=0)
        time = batteryInfo[:, 1]
        battery = batteryInfo[:, 0]
        batteryAxes.plot(time, battery)
        batteryAxes.axvline(expectedTime, linestyle='--')

        yTickSpacing = RoundHalfUpToInt((max(battery)) + 1/ 10) if max(battery) + 1 > 10 else 1
        plt.yticks(np.arange(0, max(battery) + 1, yTickSpacing))
        xTickSpacing = RoundHalfUpToInt(self.Environment.MaxTime + 1) if self.Environment.MaxTime + 1 > 10 else 1
        plt.xticks(np.arange(0, self.Environment.MaxTime + 1, xTickSpacing))

        labels = batteryAxes.get_xticklabels()
        plt.setp(labels, horizontalalignment='right')
        batteryAxes.set(xlabel='Time', ylabel='Battery Charge', title=routeName + ': Battery Charge vs Time')
        
        if routeName == "":
            plt.show()
        else:
            if not os.path.exists("temp"):
                os.mkdir('temp/')

            figure.savefig('temp/' + routeName + '_BatteryChargeVsTime.png', dpi=figure.dpi)