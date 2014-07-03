#!/usr/bin/python
# encoding: utf-8

from bitify.gpio.sensors import ds18b20
from bitify.gpio.displays import hd44780
from time import sleep

import sys


sample_period=1
degree_symbol = chr(223) # Degrees character code on the HD44780 
display_format = "{:4.1f}"
min_max_format = "Mn:"+display_format+" Mx:" + display_format
to_display = "Now: "+display_format + degree_symbol + "C" + chr(24)

display = hd44780.HD44780()
sensor = ds18b20.DS18B20(sys.argv[1]+"/w1_slave")

history=[]

try:
    while True:
        temperature = sensor.read_temperature()
        display.display_line_1(to_display.format(temperature / 1000.0))
        history.append(temperature)
        display.display_line_2( min_max_format.format(min(history)/1000.0, max(history)/1000.0) )
        sleep(1)
except KeyboardInterrupt:
    display.clear_screen()
    display.display_line_1("Monitor")
    display.display_line_2("not running")
    print "Exiting due to Ctrl+C"
