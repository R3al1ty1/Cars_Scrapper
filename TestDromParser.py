import unittest
from main import getCar


class TestDromParser(unittest.TestCase):
    def testDict(self):
        url = "https://irkutsk.drom.ru/toyota/prius/46333623.html"
        data = getCar(url)
        self.assertEqual(type(data), dict)
    def testFuelPetrol(self):
        url = "https://odintsovo.drom.ru/skoda/octavia/46333650.html"
        data = getCar(url)
        self.assertEqual(data["fuelType"], "бензин")
    def testFuelDiesel(self):
        url = "https://krasnoyarsk.drom.ru/bmw/3-series/"
        data = getCar(url)
        self.assertEqual(data["fuelType"], "дизель")
    def testPower_1(self):
        url = "https://klin.drom.ru/renault/sandero_stepway/46333979.html"
        data = getCar(url)
        self.assertEqual(data["power, hp"], 181)
    def testPower_2(self):
        url = "https://klin.drom.ru/renault/sandero_stepway/46333993.html"
        data = getCar(url)
        self.assertEqual(data["power, hp"], 69)
    def testWheelDriveRear

if __name__ == '__main__':
    unittest.main()
