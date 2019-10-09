import csv
import dateutil.parser
from os import listdir
from os.path import isfile, join
import argparse
import datetime
import math
import copy


class ImportData:
    def __init__(self, data_csv):
        self._time = []
        self._value = []
        self._file = data_csv
        self._type = 0

        if 'activity' in data_csv or 'bolus' in data_csv or 'meal' in data_csv:
            self._type = 0

        elif ('smbg' in data_csv or 'hr' in data_csv or
              'cgn' in data_csv or 'basal' in data_csv):
            self._type = 1

        # open file, create a reader from csv.DictReader,
        # and read input times and values
        with open(data_csv) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if (row['time'] == ''):
                    continue
                tm = (datetime.datetime.strptime(
                    row['time'], '%m/%d/%y %H:%M'))
                try:
                    v = float(row['value'])
                    if (not math.isnan(v)):
                        self._value.append(v)
                        self._time.append(tm)
                except ValueError:
                    print('Invalid value: ' + row['value'])

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
                low = mid + 1
            else:
                high = mid - 1

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
    round_obj = copy.deepcopy(obj)
    round_lst = []
    values = []
    time_entries = len(round_obj._time)
    for i in range(time_entries):
        tm = round_obj._time[i]
        discard = datetime.timedelta(minutes=tm.minute % res,
                                     seconds=tm.second)
        tm -= discard
        if (discard >= datetime.timedelta(
                minutes=math.ceil(res/2))):
            tm += datetime.timedelta(minutes=res)
        round_obj._time[i] = tm

    if time_entries > 0:
        round_lst.append(round_obj._time[0])
        search_result = round_obj.linear_search_value(round_obj._time[i])
        if (obj._type == 0):
            values.append(sum(search_result))
        elif (obj._type == 1):
            values.append(sum(search_result)/len(search_result))

    for i in range(1, time_entries):
        if round_obj._time[i] == round_obj._time[i - 1]:
            continue
        else:
            round_lst.append(round_obj._time[i])
            search_result = round_obj.linear_search_value(round_obj._time[i])
            if obj._type == 0:
                values.append(sum(search_result))
            elif obj._type == 1:
                values.append(sum(search_result)/len(search_result))

    return zip(round_lst, values)


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
    for obj in data_lst:
        data_5.append(roundTimeArray(obj, 5))

    data_15 = []  # a list with time rounded to 15min
    for obj in data_lst:
        data_5.append(roundTimeArray(obj, 15))

    # print to a csv file
    printArray(data_5, files_lst, args.output_file+'_5', args.sort_key)
    printArray(data_15, files_lst, args.output_file+'_15', args.sort_key)
