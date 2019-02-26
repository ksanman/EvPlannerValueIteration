from context import TripScheduler, NissanLeafBattery, RoundHalfUpToInt, Rewards, Map
from time import time

def run():
    tripScheduler = TripScheduler(Rewards())
    stGeorgeTrip = 'data/stgeorge_route.txt'
    stGeorgeChargers = 'data/stgeorge_chargers.txt'
    battery = NissanLeafBattery(30)
    tripTime = RoundHalfUpToInt((8 * 60) / 15) # Hours to 15 minute time blocks

    t = time()
    schedule = tripScheduler.ScheduleRouteFromFiles("St George Trip with Destination Charger", stGeorgeTrip, stGeorgeChargers, tripTime, battery, True)[0]
    t = time() - t

    print 'Schedule Done \n Completed in: {0} seconds'.format(t)
    print schedule.Directions

    map = Map()
    map.DrawRoute(schedule.Route, schedule.Chargers)

if __name__ == '__main__':
    run()