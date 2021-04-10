#!/bin/bash
cd ~/EZ-TS
bindir=~/bin
if ! [ -d "$bindir" ]
    then
    echo "ERROR: No $bindir directory found! to make the EZ-TS command tools easy to use either make a ~/bin directory, or edit the bindir in this ~/EZ-TS/init.sh script to a directory of your choice that is in your path"
    exit 1
else
    chmod 777 *sh EZTS-setup.py
    cp EZTS-setup.py $bindir/EZTS-setup
    cp re-configure.sh $bindir/re-configure
    cp EZTS-update.sh $bindir/EZTS-update

    sed -i '/sys_user=/d' config.py
    sed -i "/#email for job status information/i sys_user='$USER'" config.py
fi

#Make default directories to store archived config.py files, runlog and errors, but don't overwrite if already present
if ! [ -d runlog ]
    then
    mkdir runlog
fi
if ! [ -d errors ]
    then
    mkdir errors
fi
if ! [ -d archive ]
    then
    mkdir archive
fi
