#!/usr/bin/python
# encoding: utf-8
'''
Created on 29 Jun 2014

@author: bitify
'''

import os
from datetime import datetime

class DS18B20(object):
    '''
    Simple interface to read from DS18B20
    '''

    def __init__(self, device_file, log_file="temperature.log"):
        self.device_file = device_file
        self.log_file = log_file


    def read_temperature(self):
        try:
            temp_file = open(self.device_file)
            text = temp_file.read().split("\n")
            temp_file.close()
            
            if (len(text) > 0 and text[0].endswith("YES")): # We have some output
                # We have data so grab the last 5 chars of the second line (i.e. tha temperature)
                #rrdtool.update(database_file, "N:%f" % float(text[1][-5:])) 
                data_file=open(self.log_file,'a')
                temperature = text[1][-5:]
                now = datetime.now()
                data_file.write(now.strftime("%Y-%m-%d-%H:%M:%S") +" "+temperature+"\n")
                data_file.close()
                return int(temperature)
        except IOError as (errno, strerror):
                # Rough clean up, needs tidying
                temp_file.close()
                data_file.close()
                
if __name__ == "__main__":
    sensor = DS18B20("/sys/bus/w1/devices/28-000004e53685/w1_slave")
    print "{:5.1f}ºC".format((sensor.read_temperature() / 1000.0))