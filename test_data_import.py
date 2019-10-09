import unittest
import os
import datetime
import data_import


class TestDataImport(unittest.TestCase):
    def test_import_data(self):
        filename = './smallData/activity_small.csv'
        obj = data_import.ImportData(filename)
        self.assertEqual(len(obj._time), len(obj._value))

    def test_linear_search(self):
        filename = './smallData/activity_small.csv'
        obj = data_import.ImportData(filename)
        d = datetime.datetime(2018, 3, 12, 0, 0, 0, 0)
        result = obj.linear_search_value(d)
        self.assertEqual(result, [0])


if __name__ == '__main__':
    unittest.main()
