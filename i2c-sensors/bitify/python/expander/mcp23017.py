import time
import smbus

import bitify.python.utils.i2cutils as I2CUtils

class MCP23017(object):
    IODIRA = 0x00
    IPOLA = 0x02
    GPINTENA = 0x04
    DEFVALA = 0x06
    INTCONA = 0x08
    IOCON = 0x0a
    GPPUA = 0x0c
    INTFA = 0x0e
    INTCAPA = 0x10
    GPIOA = 0x12
    OLATA = 0x14
    
    IODIRB = 0x01
    IPOLB = 0x02
    GPINTENB = 0x05
    DEFVALB = 0x07
    INTCONB = 0x09
    # IOCON = 0x15 Shared register
    GPPUB = 0x0d
    INTFB = 0x0f
    INTCAPB = 0x11
    GPIOB = 0x13
    OLATB = 0x15
    
    PORTA = 0
    PORTB = 1
    
    PIN0 = 0
    PIN1 = 1
    PIN2 = 2
    PIN3 = 3
    PIN4 = 4
    PIN5 = 5
    PIN6 = 6
    PIN7 = 7
    
    def __init__(self, bus, address, name):
        '''
        Constructor
        '''
        self.bus = bus
        self.address = address
        self.name = name

    def port_config(self, port, config):
        if (port == MCP23017.PORTA):
            I2CUtils.i2c_write_byte(self.bus, self.address,MCP23017.PORTA, config)
        else:
            I2CUtils.i2c_write_byte(self.bus, self.address,MCP23017.PORTB, config)
    
    def write_port(self, port, byte):
        if (port == MCP23017.PORTA):
            I2CUtils.i2c_write_byte(self.bus, self.address,MCP23017.OLATA, byte)
        else:
            I2CUtils.i2c_write_byte(self.bus, self.address,MCP23017.OLATB, byte)

    def read_port(self, port, byte):
        if (port == MCP23017.PORTA):
            return (I2CUtils.i2c_read_byte(self.bus, self.address,MCP23017.GPIOA))
        else:
            return (I2CUtils.i2c_read_byte(self.bus, self.address,MCP23017.GPIOB))

if __name__ == "__main__":
    bus = smbus.SMBus(I2CUtils.i2c_raspberry_pi_bus_number())
    mcp23017=MCP23017(bus, 0x20, "expander-01")
     