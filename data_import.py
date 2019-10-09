import csv
import dateutil.parser
from os import listdir
from os.path import isfile, join
import argparse
import datetime


class ImportData:
    def __init__(self, data_csv):
        self._time = []
        self._value = []

        # open file, create a reader from csv.DictReader,
        # and read input times and values
        with open(data_csv) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self._time.append(row['time'])
                self._value.append(row['value'])

    def linear_search_value(self, key_time):
        # return list of value(s) associated with key_time
        # if none, return -1 and error message
        result = []
        for i in range(len(self._time)):
            if self._time[i] == key_time:
                result.append(self._value[i])
        if (len(result) == 0):
            print('Cannot find any value associated with key_time')
            return -1
        return result

    def binary_search_value(self, key_time):
        # optional extra credit
        # return list of value(s) associated with key_time
        # if none, return -1 and error message
        result = []
        low = 0
        high = len(self._time) - 1
        while low < high:
            mid = (low + high) // 2
            if (self._time[mid] == key_time):
                result.append(self._value[mid])
                left = mid - 1
                while left > 0:
                    if self._time[left] == key_time:
                        result.append(self._value[left])
                        left = left - 1
                    else:
                        break
                right = mid + 1
                while right < len(self._time):
                    if self._time[right] == key_time:
                        result.append(self._value[right])
                        right = right + 1
                    else:
                        break
            elif (self._time[mid] < key_time):
                left = mid + 1
            else:
                right = mid - 1

        if (len(result) == 0):
            print('Cannot find any value associated with key_time')
            return -1
        return result


def roundTimeArray(obj, res):
    # Inputs: obj (ImportData Object) and res (rounding resoultion)
    # objective:
    # create a list of datetime entries and associated values
    # with the times rounded to the nearest rounding resolution (res)
    # ensure no duplicated times
    # handle duplicated values for a single timestamp based on instructions in
    # the assignment
    # return: iterable zip object of the two lists
    # note: you can create additional variables to help with this task
    # which are not returned
    pass


def printArray(data_list, annotation_list, base_name, key_file):
    # combine and print on the key_file
    pass


if __name__ == '__main__':

    # adding arguments
    parser = argparse.ArgumentParser(
        description='A class to import, combine, ' +
                    'and print data from a folder.',
        prog='dataImport')

    parser.add_argument('--folder_name', type=str, help='Name of the folder')

    parser.add_argument('--output_file', type=str, help='Name of Output file')

    parser.add_argument('--sort_key', type=str, help='File to sort on')

    parser.add_argument('--number_of_files', type=int,
                        help="Number of Files", required=False)

    args = parser.parse_args()

    # pull all the folders in the file
    files_lst = listdir(args.folder_name)  # list the folders

    # import all the files into a list of ImportData objects (in a loop!)
    data_lst = []
    for f in files_lst:
        data_lst.append(ImportData(args.folder_name + '/' + f))

    # create two new lists of zip objects
    # do this in a loop, where you loop through the data_lst
    data_5 = []  # a list with time rounded to 5min
    data_15 = []  # a list with time rounded to 15min

    # print to a csv file
    printArray(data_5, files_lst, args.output_file+'_5', args.sort_key)
    printArray(data_15, files_lst, args.output_file+'_15', args.sort_key)
