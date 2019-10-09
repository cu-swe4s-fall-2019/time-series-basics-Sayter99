#!/bin/bash

test -e ssshtest || wget https://raw.githubusercontent.com/ryanlayer/ssshtest/master/ssshtest
. ssshtest

run test_style pycodestyle data_import.py
assert_no_stdout
run test_style pycodestyle test_data_import.py
assert_no_stdout
