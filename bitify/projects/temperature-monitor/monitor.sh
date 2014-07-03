#!/bin/bash

# Ensure the correct modules are loaded
/sbin/modprobe w1_gpio
/sbin/modprobe w1_therm

devices=($(ls -d /sys/bus/w1/devices/28*))
# Just use the first one
#device=$(basename ${devices[0]})
device=${devices[0]}

export PYTHONPATH="/home/pi/development/raspi/"
python monitor.py $device & > /dev/null
sudo -u pi ./run-server.sh
