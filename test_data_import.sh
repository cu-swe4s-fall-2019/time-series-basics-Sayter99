#!/bin/bash

test -e ssshtest || wget https://raw.githubusercontent.com/ryanlayer/ssshtest/master/ssshtest
. ssshtest

run test_style pycodestyle data_import.py
assert_no_stdout
run test_style pycodestyle test_data_import.py
assert_no_stdout

run bad_sort_key python data_import.py --folder_name smallData --output_file aaa --sort_key aa
assert_stdout
assert_exit_code 1

run bad_folder python data_import.py --folder_name ddd --output_file aaa --sort_key aa
assert_stdout
assert_exit_code 1

run basic_test python data_import.py --folder_name smallData --output_file aaa --sort_key hr_small.csv
assert_stdout
assert_exit_code 0
rm aaa_5.csv
rm aaa_15.csv
