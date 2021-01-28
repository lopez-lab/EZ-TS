#!/bin/bash
#check current directory and move to input
currentdir=`pwd`
if [[ "$currentdir" == *utilities* ]]
    then
    cd ../input
elif [[ "$currentdir" == *ts_guess* ]]
    then
    cd ../input
elif [[ "$currentdir" == *conf_search* ]]
    then
    cd ../input
elif [[ "$currentdir" == *conf_opt* ]]
    then
    cd ../input
elif [[ "$currentdir" == *lowest_ts* ]]
    then
    cd ../input
elif [[ "$currentdir" == *input* ]]
    then 
    :
else
    cd input
fi

#check if benchmarking was requested
benchmark=$(grep "\--benchmark" summary -c)
if [[ $benchmark -gt 0 ]]
    then
    echo "Benchmarking kept active"
    python3 ../utilities/generate-inputs.py -l ts_guess-list.txt --benchmark
    else
    python3 ../utilities/generate-inputs.py -l ts_guess-list.txt
fi
