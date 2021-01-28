#!bin/bash
    search=$(basename ${1%.*})
    
    if test -f $search-ts-energies.txt
        then 
        rm $search-ts-energies.txt
    fi
    for i in $search*log;
        do
        freq=$(grep "Frequencies" -m1 $i |awk '{ print $3 }' )
        freqint=${freq%.*}
        echo $freqint
        if [[ $freqint -lt -200 ]]
            then
            energy=$(grep "Sum of electronic and thermal Free Energies" $i | awk '{ print $8 }')
            echo $i $energy >> $search-ts-energies.txt
        fi
     done
    if test -f "$search-ts-energies.txt"
        then
        lowestenergyts=$(sort -g -k2,2 $search-ts-energies.txt | head -1 |awk '{ print $1 }')
        lowesttsenergy=$(sort -g -k2,2 $search-ts-energies.txt | head -1 |awk '{ print $2 }')
             else
         echo "No valid TS found" >> $search-ts-energies.txt
     fi
     echo "any additional invalid conformers:" >> $search-ts-energies.txt
     for i in $search*log;
        do
        freq=$(grep "Frequencies" -m1 $i |awk '{ print $3 }' )
        freqint=${freq%.*}
        echo $freqint
        if [[ $freqint -gt -200 ]]
            then
            echo "$i has an invalid negative frequency $freqint" >> $search-ts-energies.txt
        fi
     done
#if this is lowest energy guess_ts, then setup for conformational search, if this is final lowest TS move to lowest_ts
        if [[ $2 == 'ts_guess' ]]
            then
            obabel $lowestenergyts -o xyz -O ../conf_search/$search/CREST/$search.xyz
            finalfreq=$(grep "Frequencies" -m1 $lowestenergyts |awk '{ print $3 }' ) 
            finalfreqint=${finalfreq%.*}
            if [[ $finalfreqint -gt -750 ]]
               then
               sed -i '/dihedral:/d' ../conf_search/$search/CREST/$search.c 
            fi
        elif [[ $2 == 'conf_opt' ]]
            then
            if test -f ../lowest_ts/$search-lowest_ts-energies.txt
                then 
                rm ../lowest_ts/$search-lowest_ts-energies.txt
            fi
            if test -f ../ts_guess/$search-ts-energies.txt
                then 
                rottsenergy=$(sed '/any additional/q' ../ts_guess/$search-ts-energies.txt | head -n -1 | sort -g -k2,2 | head -1 |awk '{ print $2 }') 
            else
                for i in ../ts_guess/$search*log;
                    do
                    freq=$(grep "Frequencies" -m1 $i |awk '{ print $3 }' )
                    freqint=${freq%.*}
                    echo $freqint
                    if [[ $freqint -lt -200 ]]
                        then
                        energy=$(grep "Sum of electronic and thermal Free Energies" $i | awk '{ print $8 }')
                        echo $i $energy >> ../ts_guess/$search-ts-energies.txt
                    fi
                done
                if test -f "../ts_guess/$search-ts-energies.txt"
                    then
                    rottsenergy=$(sort -g -k2,2 ../ts_guess/$search-ts-energies.txt | head -1 |awk '{ print $2 }')
                else
                    echo "No valid TS found" >> ../ts_guess/$search-ts-energies.txt
                fi
                    echo "any additional invalid conformers:" >> ../ts_guess/$search-ts-energies.txt
                for i in ../ts_guess/$search*log;
                    do
                    freq=$(grep "Frequencies" -m1 $i |awk '{ print $3 }' )
                    freqint=${freq%.*}
                    echo $freqint
                    if [[ $freqint -gt -200 ]]
                        then
                        echo "$i has an invalid negative frequency $freqint" >> ../ts_guess/$search-ts-energies.txt
                    fi
                done
            fi
            ediff=$(bc <<< "($rottsenergy - $lowesttsenergy)*627.5")
            cutoff='-0.4'
            if [ 1 -eq "$(echo "${ediff} < ${cutoff}" | bc)" ]
                then
                 touch ../lowest_ts/LOWEST_TS_NOTFOUNDBYCREST-$search
                echo "MoRot TS is substantially lower than other conformers by $ediff kcal/mol: $lowestenergyts `pwd`" >>  /scratch/neal.pa/autots-errors/$search
            fi
            cp $lowestenergyts ../lowest_ts/$search.log
            echo $lowestenergyts >> ../lowest_ts/$search-lowest_ts-energies.txt
            grep "Sum of electronic and thermal Free Energies" ../lowest_ts/$search.log >> ../lowest_ts/$search-lowest_ts-energies.txt
            echo " " >> ../lowest_ts/$search-lowest_ts-energies.txt
            echo "energy difference from lowest MoRot output is $ediff kcal/mol" >> ../lowest_ts/$search-lowest_ts-energies.txt
            echo " " >> ../lowest_ts/$search-lowest_ts-energies.txt
            cat $search-ts-energies.txt >> ../lowest_ts/$search-lowest_ts-energies.txt
            echo " " >> ../lowest_ts/$search-lowest_ts-energies.txt
            echo " " >> ../lowest_ts/$search-lowest_ts-energies.txt
            echo "Copying MoRot ts guesses below:" >> ../lowest_ts/$search-lowest_ts-energies.txt
            cat ../ts_guess/$search-ts-energies.txt >> ../lowest_ts/$search-lowest_ts-energies.txt
        fi
