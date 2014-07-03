#!/usr/bin/python
# encoding: utf-8

import RPi.GPIO as GPIO
import time

class HD44780(object):
    '''
    Simple interface code for a HD44780 device, 4 bit mode.
    '''
    
    def __init__(self, RSEL=25, ENABLE=24, DATA4=23, DATA5=17, DATA6=27, DATA7=22):
        self.RSEL = RSEL
        self.ENABLE = ENABLE
        self.DATA4 = DATA4 
        self.DATA5 = DATA5
        self.DATA6 = DATA6
        self.DATA7 = DATA7
        
        self.MODE_CMD = 0
        self.MODE_DATA = 1
   
        self.DELAY = 0.00005
        
        self.LINE_1 = 0x80
        self.LINE_2 = 0xC0
        
        self.LINE_LENGTH = 16
        self.BLANK = " " * self.LINE_LENGTH
        
    
        # Now setup the GPIO header
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM) 
        GPIO.setup(self.RSEL, GPIO.OUT)
        GPIO.setup(self.ENABLE, GPIO.OUT)
        GPIO.setup(self.DATA4, GPIO.OUT)
        GPIO.setup(self.DATA5, GPIO.OUT)
        GPIO.setup(self.DATA6, GPIO.OUT)
        GPIO.setup(self.DATA7, GPIO.OUT)
    
        # First we have to set the device to 4-bit operation
        self.__send_data__(0b00110011, self.MODE_CMD)
        # Make sure we stay in 4-bit mode, number of lines to 2 and font to 5 x 8
        self.__send_data__(0b00110010, self.MODE_CMD)
        # Turn display and cursor on
        self.__send_data__(0b00001111, self.MODE_CMD)
        # Turn on auto increment of cursor  
        self.__send_data__(0b00000110, self.MODE_CMD)
        # Clear the display
        self.__send_data__(0b00000001, self.MODE_CMD)        
   
    def __send_data__(self, data, mode):
        
        # Setup device to receive either command or data
        GPIO.output(self.RSEL, mode)

        # Write the high nybble        
        GPIO.output(self.DATA7, 1 if (data & 0x80 == 0x80) else 0)
        GPIO.output(self.DATA6, 1 if (data & 0x40 == 0x40) else 0)
        GPIO.output(self.DATA5, 1 if (data & 0x20 == 0x20) else 0)
        GPIO.output(self.DATA4, 1 if (data & 0x10 == 0x10) else 0)
        self.__toggle_enable__()

        # Write the low nybble
        GPIO.output(self.DATA7, 1 if (data & 0x08 == 0x08) else 0)
        GPIO.output(self.DATA6, 1 if (data & 0x04 == 0x04) else 0)
        GPIO.output(self.DATA5, 1 if (data & 0x02 == 0x02) else 0)
        GPIO.output(self.DATA4, 1 if (data & 0x01 == 0x01) else 0)
        self.__toggle_enable__()
    
    def __toggle_enable__(self):
        time.sleep(self.DELAY)
        GPIO.output(self.ENABLE, GPIO.HIGH)
        time.sleep(self.DELAY)
        GPIO.output(self.ENABLE, GPIO.LOW)
        time.sleep(self.DELAY)

    def __display_line__(self, line, text):
        self.__send_data__(line, self.MODE_CMD)
        text = (text[0:self.LINE_LENGTH]).ljust(self.LINE_LENGTH)
        for c in range(0,self.LINE_LENGTH):
            self.__send_data__(ord(text[c]), self.MODE_DATA)
    
    def display_line_1(self, text):
        self.__display_line__(self.LINE_1, text)
    
    def display_line_2(self, text):
        self.__display_line__(self.LINE_2, text)
    
    def clear_line_1(self):
        self.display_line_1(self.BLANK)
    
    def clear_line_2(self):
        self.display_line_2(self.BLANK)
    
    def clear_screen(self):
        self.display_line_1(self.BLANK)
        self.display_line_2(self.BLANK)
        
if __name__ == '__main__':
    display = HD44780()
    display.display_line_1("Hello")
    display.display_line_2("World")
    