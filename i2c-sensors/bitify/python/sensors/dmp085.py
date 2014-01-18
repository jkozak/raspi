

class BMP085(object):
    '''
    Simple BMP085 implementation
    Datasheet: http://www.adafruit.com/datasheets/BMP085_DataSheet_Rev.1.0_01July2008.pdf
    '''
    
    CALIB_BLOCK_ADDRESS = 0xAA
    CALIB_BLOCK_SIZE = 22
    
    def __init__(self, bus, address, name, oss=3):
        '''
        Constructor
        '''
        self.bus = bus
        self.address = address
        self.name = name
        
        self.calibration = bus.read_i2c_block_data(address, CALIB_BLOCK_ADDRESS, CALIB_BLOCK_SIZE)
        self.oss = oss
        self.temp_wait_period = 0.004
        self.pressure_wait_period = 0.0255  # Conversion time


    def get_word(array, index, twos):
        val = (array[index] << 8) + array[index + 1]
        if twos:
            return twos_compliment(val)
        else:
            return val        
            
    def calculate():
        
        # The sensor has a block of factory set calibration values we need to read
        # these are then used in a length calculation to get the temperature and pressure
        # copy these into convenience variables
        ac1 = get_word(calibration, 0, True)
        ac2 = get_word(calibration, 2, True)
        ac3 = get_word(calibration, 4, True)
        ac4 = get_word(calibration, 6, False)
        ac5 = get_word(calibration, 8, False)
        ac6 = get_word(calibration, 10, False)
        b1 = get_word(calibration, 12, True)
        b2 = get_word(calibration, 14, True)
        mb = get_word(calibration, 16, True)
        mc = get_word(calibration, 18, True)
        md = get_word(calibration, 20, True)
        
        # This code is a direct translation from the datasheet
        # and should be optimised for real world use
        
        # Calculate temperature
        x1 = ((temp_raw - ac6) * ac5) / 32768
        x2 = (mc * 2048) / (x1 + md)
        b5 = x1 + x2
        t = (b5 + 8) / 16
        
        # Now calculate the pressure
        b6 = b5 - 4000 
        x1 = (b2 * (b6 * b6 >> 12)) >> 11
        x2 = ac2 * b6 >> 11
        x3 = x1 + x2
        b3 = (((ac1 * 4 + x3) << oss) + 2) >> 2 
        
        x1 = (ac3 * b6) >> 13 
        x2 = (b1 * (b6 * b6 >> 12)) >> 16 
        x3 = ((x1 + x2) + 2) >> 2 
        b4 = ac4 * (x3 + 32768) >> 15 
        b7 = (pressure_raw - b3) * (50000 >> oss)
        if (b7 < 0x80000000):
            p = (b7 * 2) / b4
        else:
            p = (b7 / b4) * 2
        x1 = (p >> 8) * (p >> 8)
        x1 = (x1 * 3038) >> 16
        x2 = (-7357 * p) >> 16
        p = p + ((x1 + x2 + 3791) >> 4)
        return(t, p)




