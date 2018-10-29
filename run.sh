#!/bin/bash
#
# run.sh
# 
# Wrapper to run h1b_counting.py to generate output files.
# Usage: either run without any arguments or with the name of the test folder under insight_testsuite/tests.
 
if [ $# -gt 1 ] ; then
    echo "Usage: $0 [TESTNAME]" >&2
    exit 1
elif [ $# -eq 1 ] ; then
    python ./src/h1b_counting.py ./insight_testsuite/tests/$1/input/h1b_input.csv ./insight_testsuite/tests/$1/output/top_10_occupations.txt ./insight_testsuite/tests/$1/output/top_10_states.txt
else
    python ./src/h1b_counting.py ./input/h1b_input.csv ./output/top_10_occupations.txt ./output/top_10_states.txt
fi