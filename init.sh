#!/bin/bash
cd ~/EZ-TS
bindir=~/bin
if ! [ -d "$bindir" ]
    then
    echo "ERROR: No $bindir directory found! to make the EZ-TS command tools easy to use either make a ~/bin directory, or edit the bindir in this ~/EZ-TS/init.sh script to a directory of your choice"
    exit 1
else
    chmod 777 *sh
    cp EZTS-setup.sh $bindir/EZTS-setup
    cp re-configure.sh $bindir/re-configure
    cp EZTS-update.sh $bindir/EZTS-update
    cp EZTS-clean.sh $bindir/EZTS-clean
    chmod 777 $bindir/EZTS-clean
    sed -i "/#email for job status information/i sysuser='$USER'" config.py
fi
