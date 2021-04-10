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
elif [[ "$currentdir" == *benchmarking* ]]
    then
    cd ../input
elif [[ "$currentdir" == *irc* ]]
    then
    cd ../input
elif [[ "$currentdir" == *irc* ]]
    then
    cd ../input

elif [[ "$currentdir" == *input* ]]
    then 
    :
else
    cd input
fi

#check if benchmarking or irc was requested

if [[ -d "../benchmarking" ]]
then
    benchmark='--benchmark'
else
    benchmark=''
fi

if [[ -d "../irc" ]]
then
    irc='--irc'
else
    irc=''
fi

python3 ../utilities/generate-inputs.py -l ts_guess-list.txt $benchmark $irc


