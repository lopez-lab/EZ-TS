#!/bin/bash
cd ~/EZ-TS
archive_date=$(date +"%Y-%m-%d-%T")
cp config.py archive/config-$archive_date.py
git reset --hard
git pull origin
bash init.sh
echo "EZ-TS up to date"
