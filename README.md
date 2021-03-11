# ad5592
## Overview
This repository contains the code to read the ADC pins on the AD5592R. Source code was provided originally by http://www.spazztech.com/ad5592-snack.html.

The original code was altered and complete files are provided here.

## ad5592_read8.c

To compile this, use the following :

*_gcc -o ad5592_read8 ad5592_read8.c -l bcm2835_*

To run the code, use the following :

*_sudo ./ad5592_read8_*
*NOTE: sudo must be used to allow access to SPI registers, otherwise you will get a segfault*


