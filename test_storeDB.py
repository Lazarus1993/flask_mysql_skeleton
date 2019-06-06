import unittest
import storeDB
from unittest.mock import patch


class TeststoreDB(unittest.TestCase):
    def test_source_website_health_gold(self):
        with patch('storeDB.requests.get') as mocked_get:
            mocked_get.return_value.ok = True
            mocked_get.return_value.text = '_Success_'

            actualResponse = storeDB.source_website_health_gold()
            mocked_get.assert_called_with('https://www.investing.com/commodities/gold-historical-data')
            self.assertEqual(actualResponse,'_Success_')
    def test_source_website_health_silver(self):
        with patch('storeDB.requests.get') as mocked_get:
            mocked_get.return_value.ok = True
            mocked_get.return_value.text = '_Success_'

            actualResponse = storeDB.source_website_health_silver()
            mocked_get.assert_called_with('https://www.investing.com/commodities/silver-historical-data')
            self.assertEqual(actualResponse,'_Success_')
    
if __name__ == '__main__':
    unittest.main()