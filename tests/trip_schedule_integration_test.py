from context import TripScheduler, NissanLeafBattery, RoundHalfUpToInt, Rewards
from time import time

def run():
    tripScheduler = TripScheduler(Rewards())
    stGeorgeTrip = 'data/stgeorge_route.txt'
    stGeorgeChargers = 'data/stgeorge_chargers.txt'
    battery = NissanLeafBattery(40)
    tripTime = RoundHalfUpToInt((8 * 60) / 15) # Hours to 15 minute time blocks

    t = time()
    schedule = tripScheduler.ScheduleRouteFromFiles("St George Trip without Destination Charger", stGeorgeTrip, stGeorgeChargers, tripTime, battery, True)
    t = time() - t

    print 'Schedule Done \n Completed in: {0} seconds'.format(t)
    print schedule

if __name__ == '__main__':
    run()