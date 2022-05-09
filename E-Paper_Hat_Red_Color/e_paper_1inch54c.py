#!/usr/bin/python
# -*- coding:utf-8 -*-

import lib_1nch54c_e_paper
import time
from PIL import Image,ImageDraw,ImageFont


try:    
    e_paper = lib_1nch54c_e_paper.epaper()
    e_paper.init()
    #e_paper.Clear_screen()
    time.sleep(1)
    
    # Drawing on the image
    black_image = Image.new('1', (e_paper.width, e_paper.height), 255)  # 255: clear the frame
    red_image = Image.new('1', (e_paper.width, e_paper.height), 255)  # 255: clear the frame
    
    font = ImageFont.truetype(('images/Font.ttc'), 28)
    font18 = ImageFont.truetype(('images/Font.ttc'), 18)
    
    draw_black = ImageDraw.Draw(black_image)
    draw_red = ImageDraw.Draw(red_image)
    #draw_black.rectangle((0, 10, 200, 34), fill = 0)
    draw_black.text((8, 12), 'hello world', font = font, fill = 0)

    e_paper.display_image(e_paper.buffer(black_image),e_paper.buffer(red_image))
    time.sleep(1)
    
    # read bmp file 
    black_image = Image.open('images/img1.bmp')
    red_image = Image.open('images/img2.bmp')    
    e_paper.display_image(e_paper.buffer(black_image),e_paper.buffer(red_image))
    time.sleep(1)
    
    e_paper.Clear_screen()
    
    e_paper.sleep()
    
except KeyboardInterrupt:    
    lib_1nch54c_e_paper.e_paper_config4.device_exit()
    exit()
