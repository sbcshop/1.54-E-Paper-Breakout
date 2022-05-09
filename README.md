# 1.54-E-Paper-Breakout

### 1.54-inch e-paper display is an Active Matrix Electrophoretic Display(AMEPD) with 200*200 resolution respectively, comes with SPI interface.e-paper breakout comes in two variant with the ability to display black-and-white or black-white-red graphics. Without power, your image will persist endlessly - display it, then turn off the electricity. These e-paper display modules don't require any power after they've been updated, and they may even be turned off completely, with the content remaining on the screen indefinitely. These e-ink screen is ideal for solar or battery-powered devices.


## Code
### First of all, you need to enable SPI in raspberry pi, for this you need to go  ```sudo raspi-config ``` then go to "interface options->SPI->yes->press enter" 
#### There are two folder in GitHub repository
 * E_Paper_B&W (Black Color)
   * e_paper_1inch54.py        -> Run this file
   * lib_1nch54_e_paper.py -> Library of 1.54 inch e-paper
   
 * E-Paper_Red_Color (Red & Black Color)
   * e_paper_1inch54c.py  -> Run this file 
   * lib_1nch54c_e_paper.py    -> Library of 1.54 inch e-paper red color
