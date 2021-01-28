#!/bin/bash
cd ~/EZTS
cp EZTS-setup.sh ~/bin/EZTS-setup
chmod 777 ~/bin/EZTS-setup
cp re-configure.sh ~/bin/re-configure
chmod 777 ~/bin/re-configure
cp EZTS-update.sh ~/bin/EZTS-update
chmod 777 ~/bin/EZTS-update
chmod 777 *sh
cp EZTS-clean.sh ~/bin/EZTS-clean
chmod 777 ~/bin/EZTS-clean
sed -i "/#local workflow variables/i user='$USER@northeastern.neu.edu'" config.py
