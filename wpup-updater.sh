#!/bin/bash
sleep 2
sudo rm /usr/bin/wpup
sudo wget -q -o /dev/null -O /usr/bin/wpup https://raw.githubusercontent.com/koyuspace/wpup/main/wpup.py?$RANDOM
sudo chmod +x /usr/bin/wpup