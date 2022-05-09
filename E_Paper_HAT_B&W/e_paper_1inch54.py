#!/usr/bin/python
# -*- coding:utf-8 -*-
import lib_1nch54_e_paper
import time
from PIL import Image,ImageDraw,ImageFont

try:
    
    e_paper = lib_1nch54_e_paper.epaper()
    e_paper.init()
    e_paper.Clear_screen(0xFF)
    
    # Drawing on the image
    image = Image.new('1', (e_paper.width, e_paper.height), 255)  # 255: clear the frame
    
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(('images/Font.ttc'), 28)
    draw.text((8, 10), 'HELLO WORLD', font = font, fill = 0)
    draw.text((10, 60), '1.54 e-paper', font = font, fill = 0)
    draw.text((60, 100), 'HAT', font = font, fill = 0)

    e_paper.display_image(e_paper.buffer(image.rotate(90)))
    time.sleep(2)
    
    # read bmp file 
    image = Image.open('images/img.bmp')
    e_paper.display_image(e_paper.buffer(image))
    time.sleep(2)

    e_paper.init()
    e_paper.Clear_screen(0xFF)
    
    e_paper.sleep()
    lib_1nch54_e_paper.e_paper_config.device_exit()
        
except KeyboardInterrupt:    
    lib_1nch54_e_paper.e_paper_config.device_exit()
    exit()
