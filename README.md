# ad5592
## Overview
This repository contains the code to read the ADC pins on the AD5592R. Source code was provided originally by http://www.spazztech.com/ad5592-snack.html.

The original code was altered and complete files are provided here.

## ad5592_read8.c


To compile this, use the following :

***gcc -o ad5592_read8 ad5592_read8.c -l bcm2835***

To run the code, use the following :

***_sudo ./ad5592_read8_***

*NOTE: sudo must be used to allow access to SPI registers, otherwise you will get a segfault*


The data will be written to a timestamped CSV file. Rename this file however you wish and use it with the readfile.py program to analyze and view data.

## readfile.py


To run this use the following:

***python3 readfile.py***


The terminal will ask you the following:


*Enter Filename:*

*Enter # Channels:*

*Enter display code (n = normal data; r = rising edges; f = frequency; code = c:*



