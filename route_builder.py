from charger_info import ChargerPoint, Point
import random

class RouteBuilder:
    def __init__(self):
        # Chargers. Each Lat/Long is 1 distance unit from the former. 
        #charger1 = ChargerInfo(0, "charger1", 0, 0, 13.3)

        # self.ChargerList = [
        #     ChargerPoint(1, "charger2", 1, 1, 13.3),
        #     ChargerPoint(2, "charger3", 2, 2, 13.3),
        #     ChargerPoint(3, "charger4", 3, 3, 13.3),
        #     ChargerPoint(4, "charger5", 4, 4, 13.3),
        #     ChargerPoint(5, "charger6", 5, 5, 13.3),
        #     ChargerPoint(6, "charger7", 6, 6, 13.3),
        #     ChargerPoint(7, "charger8", 7, 7, 13.3),
        #     ChargerPoint(8, "charger9", 8, 8, 13.3),
        #     ChargerPoint(9, "charger10", 9, 9, 13.3),
        #     ChargerPoint(10, "charger11", 10, 10, 13.3),
        #     ChargerPoint(11, "charger12", 11, 11, 13.3),
        #     ChargerPoint(12, "charger13", 12, 12, 13.3),
        #     ChargerPoint(13, "charger14", 13, 13, 13.3),
        #     ChargerPoint(14, "charger15", 14, 14, 13.3),
        #     ChargerPoint(15, "charger16", 15, 15, 13.3),
        #     ChargerPoint(16, "charger17", 16, 16, 13.3),
        #     ChargerPoint(17, "charger18", 17, 17, 13.3),
        #     ChargerPoint(18, "charger19", 18, 18, 13.3),
        #     ChargerPoint(19, "charger20", 19, 19, 13.3)
        # ]
        self.ChargerList = []
        for c in range(1, 20):
            self.ChargerList.append(ChargerPoint(c, "charger{0}".format(c), c, c, 400, 32))

    def GetChargersInOrder(self, numberOfChargers):
        return self.ChargerList[:numberOfChargers]

    def GetRandomSample(self, numberOfChargers):
        return random.sample(self.ChargerList, numberOfChargers)