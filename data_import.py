import csv
import dateutil.parser
from os import listdir
from os.path import isfile, join
import argparse
import datetime
import math
import copy
import sys
import time


class ImportData:
    def __init__(self, data_csv):
        self._time = []
        self._value = []
        self._file = data_csv
        self._type = 0

        if 'activity' in data_csv or 'bolus' in data_csv or 'meal' in data_csv:
            self._type = 0

        elif ('smbg' in data_csv or 'hr' in data_csv or
              'cgm' in data_csv or 'basal' in data_csv):
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
                    if (row['value'] == 'low'):
                        print('converting low to 40')
                        row['value'] = 40
                    elif (row['value'] == 'high'):
                        print('converting high to 300')
                        row['value'] = 300

                    v = float(row['value'])
                    if (not math.isnan(v)):
                        self._value.append(v)
                        self._time.append(tm)
                except ValueError:
                    print('Invalid value: ' + row['value'])

        if (len(self._time) > 0):
            if (self._time[-1] < self._time[0]):
                self._time.reverse()
                self._value.reverse()

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
        mid = -1
        while low <= high:
            mid = (low + high) // 2
            if (self._time[mid] == key_time):
                break
            elif (self._time[mid] < key_time):
                low = mid + 1
            else:
                high = mid - 1

        result.append(self._value[mid])
        left = mid - 1
        while left >= 0:
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
        search_result = round_obj.binary_search_value(round_obj._time[0])
        if (obj._type == 0):
            values.append(sum(search_result))
        elif (obj._type == 1):
            values.append(sum(search_result)/len(search_result))

    for i in range(1, time_entries):
        if round_obj._time[i] == round_obj._time[i - 1]:
            continue
        else:
            round_lst.append(round_obj._time[i])
            search_result = round_obj.binary_search_value(round_obj._time[i])
            if obj._type == 0:
                values.append(sum(search_result))
            elif obj._type == 1:
                values.append(sum(search_result)/len(search_result))

    return zip(round_lst, values)


def printArray(data_list, annotation_list, base_name, key_file):
    data_list1 = []
    data_list2 = []
    annotation_list1 = []
    annotation_list2 = []
    # combine and print on the key_file
    if not (key_file in annotation_list):
        print('Cannot find sort_key')
        return -1
    else:
        for i in range(len(annotation_list)):
            if (annotation_list[i] == key_file):
                annotation_list1.append(annotation_list[i])
                data_list1.append(data_list[i])
            else:
                annotation_list2.append(annotation_list[i])
                data_list2.append(data_list[i])

    attributes = ['time', key_file] + annotation_list2
    with open(base_name + '.csv', mode='w') as output:
        writer = csv.writer(output, delimiter=',')
        writer.writerow(attributes)
        for (t, v) in data_list1[0]:
            rest_values = []
            for data in data_list2:
                old_len = len(rest_values)
                for (zt, zv) in data:
                    if (t == zt):
                        rest_values.append(zv)
                if (len(rest_values) == old_len):
                    rest_values.append(0)
            writer.writerow([t, v] + rest_values)


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
    try:
        files_lst = listdir(args.folder_name)  # list the folders
    except (FileNotFoundError, NameError) as e:
        print('Cannot find folder')
        sys.exit(1)

    # import all the files into a list of ImportData objects (in a loop!)
    data_lst = []
    for f in files_lst:
        data_lst.append(ImportData(args.folder_name + '/' + f))

    if (len(data_lst) == 0):
        print('no valid data')
        sys.exit(1)

    # create two new lists of zip objects
    # do this in a loop, where you loop through the data_lst
    start_time = time.time()
    data_5 = []  # a list with time rounded to 5min
    for obj in data_lst:
        data_5.append(roundTimeArray(obj, 5))
    end_time = time.time()
    print('data_5:')
    print(end_time - start_time)

    start_time = time.time()
    data_15 = []  # a list with time rounded to 15min
    for obj in data_lst:
        data_15.append(roundTimeArray(obj, 15))
    end_time = time.time()
    print('data_15:')
    print(end_time - start_time)

    # print to a csv file
    r = printArray(data_5, files_lst, args.output_file+'_5', args.sort_key)
    if (r == -1):
        sys.exit(1)

    r = printArray(data_15, files_lst, args.output_file+'_15', args.sort_key)
    if (r == -1):
        sys.exit(1)
