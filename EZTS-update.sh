#!/bin/bash
cd ~/EZTS
git reset --hard
git pull origin
bash init.sh
echo "EZTS up to date"
