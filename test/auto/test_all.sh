#!/usr/bin/bash

tests=$(find | grep '\.py$')

success=0
for test in $tests
do
    echo "Testing $test"
    python $test
    if [ ! $? -eq 0 ]
    then
	success = 1
	echo "Failed! Stopping tests"
    fi
done

if [ success ]
then
    echo "Ok: all tests succeeded"
fi
