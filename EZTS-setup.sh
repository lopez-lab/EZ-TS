#!/bin/bash

#This is a helper script for the main heavy lifter generate_input.py. It gathers the input files and provides the necessary flags for generate_input.py

#Parse some options for reading SMILES file or doing benchmarking
OPTIND=1         # Reset in case getopts has been used previously in the shell.

benchmarking_flag=''
smiles=''
optstring=":s:b"

while getopts $optstring arg; do
  case "${arg}" in

    b) benchmarking_flag='--benchmark' ;;
    s) smiles="${OPTARG}" ;;
    ?) echo "Invalid option: -${OPTARG}." ;;
  esac
done

#If reading from smiles file, generate xyz coordinates
if [ -n "$smiles" ]
    then
    echo "Reading smiles from $smiles"
    echo ""
    python3 ~/EZ-TS/smiles23D.py $smiles
    
#unfortunately a bit messy to convert to pdb then xyz, and temporarily store the charge in a charge file... but this gets the job done with minimal bash/python clash
    for i in *.pdb; do charge=$(cat ${i%.*}.charge); obabel $i --addtotitle " charge=$charge" -o xyz -O ${i%.*}.xyz; rm $i; rm ${i%.*}.charge; done
fi

#Set up directories: conf_opt  conf_search  input  lowest_ts  ts_guess  utilities
workdir=`pwd`

#If there is a previous workflow here, reset the local workflow variables, but don't overwrite everything
if test -f input/ts_guess-list.txt
    then
    sed -i '1,/#local workflow variables/!d' utilities/config.py

#Check for log files in the directory and build setup.py input list
elif compgen -G "*log" > /dev/null
    then
    mkdir utilities
    mkdir input
    mkdir ts_guess
    mkdir conf_search
    mkdir conf_opt
    mkdir lowest_ts
    mv *log input/
    #change names of input files that match keywords used by EZ-TS
    rename "tier" "TIER" input/*log
    rename "tier" "TIER" input/*xyz
    rename "conf" "CONF" input/*log
    rename "conf" "CONF" input/*xyz
    for i in input/*log
        do
        echo -e "$workdir/$i V1 175 R1   90 R2   0\n$workdir/$i V1 175 R1   90 R2 180\n$workdir/$i V1 175 R1  180 R2  90\n$workdir/$i V1 175 R1  180 R2 180\n$workdir/$i V1 175 R1  -90 R2   0\n$workdir/$i V1 175 R1  -90 R2  90" >> input/ts_guess-list.txt
        echo -e "$workdir/$i V2 175 R1   90 R2   0\n$workdir/$i V2 175 R1   90 R2 180\n$workdir/$i V2 175 R1  180 R2  90\n$workdir/$i V2 175 R1  180 R2 180\n$workdir/$i V2 175 R1  -90 R2   0\n$workdir/$i V2 175 R1  -90 R2  90" >> input/ts_guess-list.txt
    done

#Check for xyz files in the directory and build setup.py input list
elif compgen -G "*xyz" > /dev/null
    then
    mkdir utilities
    mkdir input
    mkdir ts_guess
    mkdir conf_search
    mkdir conf_opt
    mkdir lowest_ts
    mv *xyz input/
    #change names of input files that match keywords used by EZ-TS
    rename "tier" "TIER" input/*log
    rename "tier" "TIER" input/*xyz
    rename "conf" "CONF" input/*log
    rename "conf" "CONF" input/*xyz
    for i in input/*xyz
        do
        echo -e "$workdir/$i V1 175 R1   90 R2   0\n$workdir/$i V1 175 R1   90 R2 180\n$workdir/$i V1 175 R1  180 R2  90\n$workdir/$i V1 175 R1  180 R2 180\n$workdir/$i V1 175 R1  -90 R2   0\n$workdir/$i V1 175 R1  -90 R2  90" >> input/ts_guess-list.txt
        echo -e "$workdir/$i V2 175 R1   90 R2   0\n$workdir/$i V2 175 R1   90 R2 180\n$workdir/$i V2 175 R1  180 R2  90\n$workdir/$i V2 175 R1  180 R2 180\n$workdir/$i V2 175 R1  -90 R2   0\n$workdir/$i V2 175 R1  -90 R2  90" >> input/ts_guess-list.txt
    done

#If no log or xyz files can be found
else
    echo "EZ-TS"
    echo " "
    echo "Error while setting up EZ-TS"
    echo "There is no log file, xyz, smiles file, or existing EZ-TS in this directory"
    echo " "
    exit 1
fi

#Now that input dir is created, move smiles file inside if needed
if [ -n "$smiles" ]
    then
    mv $smiles input/
fi

echo "Setup command options used for this run: $benchmarking_flag $smiles" > ./input/summary

cp ~/EZ-TS/config.py  utilities/
cp ~/EZ-TS/generate-inputs.py utilities/
cp ~/EZ-TS/get-lowest.sh utilities/
cp ~/EZ-TS/start.sh ./
cp ~/EZ-TS/xyz2com.py utilities/
cp ~/EZ-TS/orca2xyz.py utilities/

echo "maindir='$workdir'" >> utilities/config.py
echo "utilities='$workdir/utilities'" >> utilities/config.py
echo "ts_guess='$workdir/ts_guess'" >> utilities/config.py
echo "conf_search='$workdir/conf_search'" >> utilities/config.py
echo "lowest_ts='$workdir/lowest_ts'" >> utilities/config.py
echo "conf_opt='$workdir/conf_opt'" >> utilities/config.py
echo "inputdir='$workdir/input'" >> utilities/config.py

cd input
python3 ../utilities/generate-inputs.py -l ts_guess-list.txt $benchmarking_flag
