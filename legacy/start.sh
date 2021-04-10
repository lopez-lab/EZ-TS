#!/bin/bash
if compgen -G "input/*log" > /dev/null
    then
    for i in input/*log
        do
        file=$(basename ${i%.*})
        ID=$(sbatch --parsable ts_guess/$file-submit.sbatch)
        echo "submitted autots workflow - $i"
    done
else
    for i in input/*xyz
        do
        file=$(basename ${i%.*})
        ID=$(sbatch --parsable ts_guess/$file-submit.sbatch)
        echo "submitted autots workflow - $i"
    done
fi
touch status.txt

