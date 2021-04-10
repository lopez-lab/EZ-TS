#!/bin/bash



#If there is a previous workflow here, reset the local workflow variables, but don't overwrite everything
if test -f input/ts_guess-list.txt
    then
    sed -i '1,/#local workflow variables/!d' utilities/config.py
    cp ~/EZ-TS/generate-inputs.py utilities/
    cp ~/EZ-TS/get-lowest.sh utilities/
    cp ~/EZ-TS/get-lowest.py utilities/
    cp ~/EZ-TS/start.sh ./
    cp ~/EZ-TS/xyz2com.py utilities/
    cp ~/EZ-TS/orca2xyz.py utilities/
    cp ~/EZ-TS/EZ-TS-setup.py utilities/

else
    #don't override the entire config file if workflow already exists, just update scripts
    mkdir utilities
    cp ~/EZ-TS/config.py utilities/
    cp ~/EZ-TS/EZ-TS-setup.py utilities/
fi

echo "main_dir='$workdir'" >> utilities/config.py
echo "utilities_dir='$workdir/utilities'" >> utilities/config.py
echo "ts_guess_dir='$workdir/ts_guess'" >> utilities/config.py
echo "conf_search_dir='$workdir/conf_search'" >> utilities/config.py
echo "lowest_ts_dir='$workdir/lowest_ts'" >> utilities/config.py
echo "conf_opt_dir='$workdir/conf_opt'" >> utilities/config.py
echo "input_dir='$workdir/input'" >> utilities/config.py
echo "benchmark_dir='$workdir/benchmarking'" >> utilities/config.py
echo "irc_dir='$workdir/irc'" >> utilities/config.py
echo "reactants_dir='$workdir/reactants'" >> utilities/config.py


python3 $#

