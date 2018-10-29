#!/bin/bash
#
# run.sh
# 
# Wrapper to run h1b_counting.py to generate output files.
# Usage: ./run.sh [-d] [-t TESTNAME]
# -d flag turns on debugging.
# -t flag uses TESTNAME as the name of the test folder under insight_testsuite/tests. If not provided, input/h1b_input.csv is used as a default.
 
debug=""

while [[ $# -gt 0 ]]
do
    key="$1"
    case $key in
        -d)
            debug="True"
            shift
            ;;
        -t)
            path="$2"
            shift
            shift
            ;;
        *)
            echo "Usage: $0 [-d] [-t TESTNAME]" >&2
            exit 1
    esac
done

if [ -z $path ] ; then
    echo "Executing python ./src/h1b_counting.py ./input/h1b_input.csv ./output/top_10_occupations.txt ./output/top_10_states.txt $debug"
    python ./src/h1b_counting.py ./input/h1b_input.csv ./output/top_10_occupations.txt ./output/top_10_states.txt $debug
else
    echo "Executing python ./src/h1b_counting.py ./insight_testsuite/tests/$path/input/h1b_input.csv ./insight_testsuite/tests/$path/output/top_10_occupations.txt ./insight_testsuite/tests/$path/output/top_10_states.txt"
    python ./src/h1b_counting.py ./insight_testsuite/tests/$path/input/h1b_input.csv ./insight_testsuite/tests/$path/output/top_10_occupations.txt ./insight_testsuite/tests/$path/output/top_10_states.txt $debug
fi
    