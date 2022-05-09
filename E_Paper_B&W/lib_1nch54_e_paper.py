import RPi.GPIO
import spidev
import time

# Display resolution
width       = 200
height      = 200

class epaper_config:
    # Pin definition of e-paper hat
    rst         = 17
    dc          = 25
    cs          = 8
    busy        = 24

    def __init__(self):
        self.GPIO = RPi.GPIO

        self.SPI = spidev.SpiDev(0, 0)

    def digital_write(self, pin, value):
        self.GPIO.output(pin, value)

    def digital_read(self, pin):
        return self.GPIO.input(pin)
    
    def spi_write(self, data):
        self.SPI.writebytes(data)
        
    def delay(self, delaytime):
        time.sleep(delaytime / 1000.0)



    def module_init(self):
        self.GPIO.setmode(self.GPIO.BCM)
        self.GPIO.setwarnings(False)
        self.GPIO.setup(self.rst, self.GPIO.OUT)
        self.GPIO.setup(self.dc, self.GPIO.OUT)
        self.GPIO.setup(self.cs, self.GPIO.OUT)
        self.GPIO.setup(self.busy, self.GPIO.IN)
        self.SPI.max_speed_hz = 4000000
        self.SPI.mode = 0b00
        return 0

    def device_exit(self):
        self.SPI.close()
        self.GPIO.output(self.rst, 0)
        self.GPIO.output(self.dc, 0)

        self.GPIO.cleanup()


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
        e_paper_config.delay(300) 
        e_paper_config.digital_write(self.reset_pin, 0)
        e_paper_config.delay(10)
        e_paper_config.digital_write(self.reset_pin, 1)
        e_paper_config.delay(300)
        
    def send_data(self, data):
        e_paper_config.digital_write(self.dc, 1)
        e_paper_config.digital_write(self.cs, 0)
        e_paper_config.spi_write([data])
        e_paper_config.digital_write(self.cs, 1)
        
    def send_command(self, command):
        e_paper_config.digital_write(self.dc, 0)
        e_paper_config.digital_write(self.cs, 0)
        e_paper_config.spi_write([command])
        e_paper_config.digital_write(self.cs, 1)


        
    def ReadBusy(self):
        while(e_paper_config.digital_read(self.busy) == 1):
            e_paper_config.delay(100)

    def Turn_On_Display(self):
        self.send_command(0x22)
        self.send_data(0xF7)
        self.send_command(0x20) 
        
        self.ReadBusy()

    def init(self):
        if (e_paper_config.module_init() != 0):
            return -1
            
        self.reset()
        
        self.ReadBusy()
        self.send_command(0x12) # SWRESET
        self.ReadBusy()
        
        self.send_command(0x01) 
        self.send_data(0xC7) 
        self.send_data(0x00) 
        self.send_data(0x01) 
        
        self.send_command(0x11) # data entry mode
        self.send_data(0x01)
        
        self.send_command(0x44) 
        self.send_data(0x00)
        self.send_data(0x18) 
        
        self.send_command(0x45) 
        self.send_data(0xC7) 
        self.send_data(0x00)
        self.send_data(0x00)
        self.send_data(0x00)

        # set RAM x address count to 0;
        self.send_command(0x4E) 
        self.send_data(0x00)

         # set RAM y address count to 0X199;
        self.send_command(0x4F)
        self.send_data(0xC7)
        self.send_data(0x00)
                
    def Clear_screen(self, color):
        self.send_command(0x24)
        for j in range(0, self.height):
            for i in range(0, int(self.width / 8)):
                self.send_data(color)
        self.Turn_On_Display()
        
    def buffer(self, image):
        buff = [0xFF] * (int(self.width/8) * self.height)
        image_monocolor = image.convert('1')
        image_width, image_height = image_monocolor.size
        pixels = image_monocolor.load()

        # Horizontal image
        if(image_width == self.width and image_height == self.height):
            for y in range(image_height):
                for x in range(image_width):
                    # Set the bits for the column of pixels at the current position.
                    if pixels[x, y] == 0:
                        buff[int((x + y * self.width) / 8)] &= ~(0x80 >> (x % 8))
                        
        #  Vertical image
        elif(image_width == self.height and image_height == self.width):
            for y in range(image_height):
                for x in range(image_width):
                    newx = y
                    newy = self.height - x - 1
                    if pixels[x, y] == 0:
                        buff[int((newx + newy*self.width) / 8)] &= ~(0x80 >> (y % 8))
        return buff

    def display_image(self, image):   
        self.send_command(0x24)
        for j in range(0, self.height):
            for i in range(0, int(self.width / 8)):
                self.send_data(image[i + j * int(self.width / 8)])   
        self.Turn_On_Display()

    def sleep(self):
        self.send_command(0x10) 
        self.send_data(0x01)
