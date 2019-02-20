from context import Optimizer, LinearSimpleBattery, Router, Point, Start, Charger, Destination, AddressInfo, TripBuilder, RoundHalfUpToInt, SimpleRewards, RealisticSimpleBattery
import unittest

class EvScheduleIntegrationTest(unittest.TestCase):
    def setUp(self):
        self.RouteBuilder = Router()
        self.TripBuilder = TripBuilder()
        self.Optimizer = Optimizer(SimpleRewards())

    def BuildTrip(self, name, stops, time, battery):
        time = time
        for c in stops[1:]:
            time += abs(c.AddressInfo.Latitude - stops[stops.index(c) - 1].AddressInfo.Latitude)

        return self.TripBuilder.BuildTestTrip(name, stops, time,  battery)

    def BuildSimpleTestCase(self, name, numberOfStops, time, battery, destinationHasCharger):
        route = [Point(AddressInfo(lat=0, long=0, title="Start"))]
        if destinationHasCharger:
            chargers = self.RouteBuilder.GetTestChargersInOrder(numberOfStops)
        else:
            chargers = self.RouteBuilder.GetTestChargersInOrder(numberOfStops - 1)
            chargers.append(Point(AddressInfo(lat=1,long=1, title="End")))

        route.extend(chargers)

        return self.BuildTrip(name, route, time, battery)

    def BuildLongTestCase(self, name, numberOfStops, time, battery, destinationHasCharger):
        route = [Point(AddressInfo(lat=0, long=0, title="Start"))]

        if destinationHasCharger:
            chargers = self.RouteBuilder.GetTestChargersInOrder(numberOfStops)
        else:
            chargers = self.RouteBuilder.GetTestChargersInOrder(numberOfStops - 1)
            chargers.append(Point(AddressInfo(lat=1,long=1, title="End")))

        route.extend(chargers)

        return self.BuildTrip(name, route, RoundHalfUpToInt(time * 1.25), battery)

    def test_SimpleTestWithChargerAtDestination(self):
        # Simple Test Case with Charger at end
        trip = self.BuildSimpleTestCase("Test Case 1", 3, 1, LinearSimpleBattery(3), True)
        schedule = self.Optimizer.OptimizeRoutes([trip], False)
        print schedule
        expected = {'Success': {'Battery': 0, 'Trip Time': '45 Minutes (3 time steps)', 'Charging Stops': []}}
        self.assertDictEqual(schedule[0], expected)

    def test_SimpleTestWithoutChargerAtDestination(self):
        # Simple Test Case with Charger not at end
        trip = self.BuildSimpleTestCase("Test Case 2", 3, 1, LinearSimpleBattery(3), False)
        schedule = self.Optimizer.OptimizeRoutes([trip], False)
        print schedule
        expected = {'Success': {'Battery': 1, 'Trip Time': '60 Minutes (4 time steps)', 'Charging Stops': ['Stop at Charger2 for 15 minutes (1 time steps).']}}
        self.assertDictEqual(schedule[0], expected)

    def test_LongSimpleTestWithChargerAtDestination(self):
        # Simple Test Case with Random Chargers and Charger at end
        trip = self.BuildLongTestCase("Test Case  3", 10, 0, RealisticSimpleBattery(10), True)
        schedule = self.Optimizer.OptimizeRoutes([trip], False)
        print schedule
        expected = {'Success': {'Battery': 3, 'Trip Time': '285 Minutes (19 time steps)', 'Charging Stops': ['Stop at Charger7 for 15 minutes (1 time steps).', 'Stop at Charger8 for 15 minutes (1 time steps).']}}
        self.assertDictEqual(schedule[0], expected)

    def test_LongSimpleTestWithoutChargerAtDestination(self):
        # Simple Test Case with Random Chargers and Charger not at end
        trip = self.BuildLongTestCase("Test Case 4", 10, 0, RealisticSimpleBattery(10), False)
        schedule = self.Optimizer.OptimizeRoutes([trip], False)
        print schedule
        expected = {'Success': {'Battery': 1, 'Trip Time': '435 Minutes (29 time steps)', 'Charging Stops': ['Stop at Charger7 for 15 minutes (1 time steps).', 'Stop at Charger8 for 15 minutes (1 time steps).', 'Stop at Charger9 for 150 minutes (10 time steps).']}}
        self.assertDictEqual(schedule[0], expected)

if __name__ == '__main__':
    unittest.main(exit=False)