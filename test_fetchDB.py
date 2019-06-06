import unittest
import fetchDB

class TestfetchDB(unittest.TestCase):
    def test_fetchFromDB(self):
        #The test for when the dates are in range of existing pricing
        result = fetchDB.fetchFromDB("2019-05-10","2019-05-22","gold")
        expectedDict = {"data": {"2019-05-22": 1274.2, "2019-05-21": 1273.2, "2019-05-20": 1277.3, "2019-05-17": 1275.7, "2019-05-16": 1286.2, "2019-05-15": 1297.8, "2019-05-14": 1296.3, "2019-05-13": 1301.8}, "mean": "1285.31", "variance": "122.01"}
        self.assertEqual(result, expectedDict)
        #The test for when the dates are not in range of existing pricing
        result = fetchDB.fetchFromDB("2020-05-10","2020-05-22","gold")
        expectedDict = {"data": {}, "mean": "0.0", "variance": "0.0"}
        self.assertEqual(result, expectedDict)
        #The test for when the start date is after end date
        result = fetchDB.fetchFromDB("2020-06-10","2020-05-22","gold")
        expectedDict = {"data": {}, "mean": "0.0", "variance": "0.0"}
        self.assertEqual(result, expectedDict)
        #The test for when the commodity is not in DB
        result = fetchDB.fetchFromDB("2020-05-10","2020-05-22","bronze")
        expectedDict = {"data": {}, "mean": "0.0", "variance": "0.0"}
        self.assertEqual(result, expectedDict)

if __name__ == '__main__':
    unittest.main()