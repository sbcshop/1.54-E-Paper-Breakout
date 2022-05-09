# Library of 1.54 e-paper HAT

import time
import spidev
import RPi.GPIO


# display_image resolution
width       = 200
height      = 200


class epaper_config:
    # Pin definition of e-paper HAT
    rst         = 17
    dc          = 25
    cs          = 8
    busy        = 24

    def __init__(self):
        self.GPIO = RPi.GPIO
        self.SPI = spidev.SpiDev()


    def digital_read(self, pin):
        return self.GPIO.input(pin)
    
    def digital_write(self, pin, value):
        self.GPIO.output(pin, value)
    
    def spi_writebyte(self, data):
        self.SPI.writebytes(data)
        
    def delay_ms(self, delaytime):
        time.sleep(delaytime / 1000.0)

    def spi_writebyte2(self, data):
        self.SPI.writebytes2(data)

    def device_init(self):
        self.GPIO.setmode(self.GPIO.BCM)
        self.GPIO.setwarnings(False)
        self.GPIO.setup(self.rst, self.GPIO.OUT)
        self.GPIO.setup(self.dc, self.GPIO.OUT)
        self.GPIO.setup(self.cs, self.GPIO.OUT)
        self.GPIO.setup(self.busy, self.GPIO.IN)

        # SPI device, bus = 0, device = 0
        self.SPI.open(0, 0)
        self.SPI.max_speed_hz = 4000000
        self.SPI.mode = 0b00
        return 0

    def device_exit(self):
        self.SPI.close()

        self.GPIO.output(self.rst, 0)
        self.GPIO.output(self.dc, 0)

        self.GPIO.cleanup([self.rst, self.dc, self.cs, self.busy])

e_paper_config = epaper_config()

class epaper:
    def __init__(self):
        self.reset_pin = e_paper_config.rst
        self.dc = e_paper_config.dc
        self.busy = e_paper_config.busy
        self.cs = e_paper_config.cs
        self.width = width
        self.height = height

    # Hardware reset
    def reset(self):
        e_paper_config.digital_write(self.reset_pin, 1)
        e_paper_config.delay_ms(200) 
        e_paper_config.digital_write(self.reset_pin, 0) 
        e_paper_config.delay_ms(5)
        e_paper_config.digital_write(self.reset_pin, 1)
        e_paper_config.delay_ms(200)   

    def send_command(self, command):
        e_paper_config.digital_write(self.dc, 0)
        e_paper_config.digital_write(self.cs, 0)
        e_paper_config.spi_writebyte([command])
        e_paper_config.digital_write(self.cs, 1)

    def send_data(self, data):
        e_paper_config.digital_write(self.dc, 1)
        e_paper_config.digital_write(self.cs, 0)
        e_paper_config.spi_writebyte([data])
        e_paper_config.digital_write(self.cs, 1)
        
    def Read_Busy(self):
        while(e_paper_config.digital_read(self.busy) == 1):
            e_paper_config.delay_ms(100)    
        
    def init(self):
        if (e_paper_config.device_init() != 0):
            return -1
        # EPD hardware init start
        self.reset()
        
        self.Read_Busy()   
        self.send_command(0x12)  
        self.Read_Busy()   

        self.send_command(0x01) #Driver output control      
        self.send_data(0xC7)
        self.send_data(0x00)
        self.send_data(0x01)
        
        self.send_command(0x11)     
        self.send_data(0x01)
    
        #set Ram-X address start/end position
        self.send_command(0x44)   
        self.send_data(0x00)
        self.send_data(0x18)    

        #set Ram-Y address start/end position 
        self.send_command(0x45)          
        self.send_data(0xC7)    
        self.send_data(0x00)
        self.send_data(0x00)
        self.send_data(0x00) 

        return 0

    def buffer(self, image):
        buff = [0xFF] * int(self.width * self.height / 8)
        image_monocolor = image.convert('1')
        image_width, image_height = image_monocolor.size
        if image_width != self.width or image_height != self.height:
            raise ValueError('Image must be same dimensions as display_image \
                ({0}x{1}).' .format(self.width, self.height))

        pixels = image_monocolor.load()
        for y in range(self.height):
            for x in range(self.width):
                # Set the bits for the column of pixels at the current position.
                if pixels[x, y] == 0:
                    buff[int((x + y * self.width) / 8)] &= ~(0x80 >> (x % 8))
        return buff

    def display_image(self, black_image, red_image):
        
        # send black image
        if (black_image != None):
            self.send_command(0x24) 
            for i in range(0, int(self.width * self.height / 8)):
                self.send_data(black_image[i])
                
        # send red image        
        if (red_image != None):
            self.send_command(0x26) 
            for i in range(0, int(self.width * self.height / 8)):
                self.send_data(~red_image[i])
                
        # display_image_REFRESH
        self.send_command(0x22) 
        self.send_data(0xF7)
        
        self.send_command(0x20) 
        self.Read_Busy()
        

    def Clear_screen(self):
        self.send_command(0x24) # DATA_START_TRANSMISSION_1
        for i in range(0, int(self.width * self.height / 8)):
            self.send_data(0xFF)
            
        self.send_command(0x26) # DATA_START_TRANSMISSION_2
        for i in range(0, int(self.width * self.height / 8)):
            self.send_data(0x00)

        self.send_command(0x22) # display_image_REFRESH
        self.send_data(0xF7)

    def sleep(self):
        self.send_command(0x10) #enter deep sleep
        self.send_data(0x01) 

        e_paper_config.delay_ms(1000)
        e_paper_config.device_exit()


