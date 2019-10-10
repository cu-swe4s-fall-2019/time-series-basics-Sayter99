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

    def test_binary_search(self):
        filename = './smallData/activity_small.csv'
        obj = data_import.ImportData(filename)
        d = datetime.datetime(2018, 3, 12, 0, 0, 0, 0)
        result = obj.linear_search_value(d)
        self.assertEqual(result, [0])

    def test_import_robustness(self):
        filename = './smallData/cgm_small.csv'
        print('Replacing 40 with low and 300 with high')
        with open(filename, "rt") as fin:
            with open("out.csv", "wt") as fout:
                for line in fin:
                    line = line.replace('40', 'low')
                    line = line.replace('300', 'high')
                    fout.write(line)
        obj = data_import.ImportData('out.csv')
        self.assertEqual(len(obj._time), len(obj._value))
        os.remove('out.csv')

    def test_round_time(self):
        filename = './smallData/cgm_small.csv'
        obj = data_import.ImportData(filename)
        z = data_import.roundTimeArray(obj, 5)
        for (t, v) in z:
            self.assertEqual(v, 131)
            self.assertEqual(t.minute, 5)
            break

        z = data_import.roundTimeArray(obj, 30)
        for (t, v) in z:
            self.assertEqual(v, (131 + 138 + 144) / 3)
            self.assertEqual(t.minute, 0)
            break

    def test_print_array(self):
        files_lst = os.listdir('smallData')
        data_lst = []
        for f in files_lst:
            data_lst.append(data_import.ImportData('smallData/' + f))

        data_5 = []
        for obj in data_lst:
            data_5.append(data_import.roundTimeArray(obj, 5))

        r = data_import.printArray(data_5, files_lst, 'out_5', 'hr_small.csv')
        self.assertNotEqual(r, -1)
        self.assertTrue(os.path.exists('out_5.csv'))
        os.remove('out_5.csv')


if __name__ == '__main__':
    unittest.main()
