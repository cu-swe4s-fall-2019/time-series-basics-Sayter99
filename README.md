# time-series-basics
Time Series basics - importing, cleaning, printing to csv
*Note date files are synthetic data.*

## Continuous Integration Status
![](https://travis-ci.com/cu-swe4s-fall-2019/time-series-basics-Sayter99.svg?branch=master)

## Installation
To use this package, you need to have [Python3](https://www.python.org/download/releases/3.0/) in your environment. And the used packages are listed below.

### Used Packages
* os
* sys
* csv
* math
* time
* datetime
* argparse
* unittest
* pycodestyle

## Usage
`data_import.py` is the main program for generating integrated csv files.
Examples of using `data_import.py` with `smallData`:
* `python data_import.py --folder_name smallData --output_file out --sort_key hr_small.csv`
* `python data_import.py --folder_name smallData --output_file out --sort_key cgm_small.csv`

### ImportData Class
* Inputs: a filename of csv file which contains `time` and `value` attributes
* Attributes:
  * time: a list containing datetimes
  * value: a list containing values
  * file: filename
* Action: filling `time` and `value` from csv file to class attributes
* Output: the processed object
* Functions:
  * linear_search_value:
    * Return list of value(s) associated with key_time. If none, return -1 and error message
  * binary_search_value:
    * Same as linear_search_value, but implemented with binary search algorithm

### roundTimeArray(obj, res)
* Inputs: `obj` (ImportData Object) and `res` (rounding resoultion)
* objective:
  * create a list of datetime entries and associated values with the times rounded to the nearest rounding resolution (res).
  * ensure no duplicated times
  * handle duplicated values for a single timestamp based on instructions in the assignment
    * Activity - sum the values
    * Bolus - sum the values
    * Meal - sum the values
    * Smbg - average the values
    * Hr - average the values
    * Cgm - average the values
    * Basal - average the values
* Output: iterable zip object of the two lists

### printArray(data_list, annotation_list, base_name, key_file)
* Inputs​: 
  * `​data_list` ​a list of zip objects of data (time, value) pairs.
  * `annotation_list` ​a list of strings with column labels for the data value
  * `base_name` ​the file name you want to print as
  * `key_file` ​the name from annotation_list you want to align the data on
* Action​: Create a csv which aligns the data in your list of zip objects based onkey_file. The first column is time, the second column is the datafrom `key_file`, the remaining headings follows the order of `os.listdir` API.
* Output: create a csv file labeled `base_name.csv`

## Changes
* Added both functional tests (`test_data_import.sh`) and unit tests (`test_data_import.py`)
* Completed class `ImportData`, `roundTimeArray`, `printArray` as mentioned before
* Tested and developed iteratively
* Profiling and benchmarking the programs
* Modified `travis.yaml` to carry out added tests
* Complete the `README.md` with performance analysis

## Profiling and Benchmarking (Extra Credit)
Benchmark time taken to create `​data_5` ​and `data_15`​ when using `binary_search_value​` inside of ​`roundTimeArray​` versus `linear_search_value​`.

### Results of time.time() function
In this section, I measured the target parts of each version.

* linear search:
  * data_5: **5.09114193916** sec
  * data_15: **2.04403114319** sec

* binary search:
  * data_5: **0.358065843582** sec
  * data_15: **0.377372980118** sec
