# Motor Bringup 

## Description
### This folder contains the code which will be used for testing and bringup of the motor

## Compiling C library
The C code must be compiled as an .so in order for the python ctypes library to access it.

To compile:

*gcc -o -shared motor_spi_lib.so motor_spi_lib.c -l bcm2835*

**NOTE:** In order to compile and run this code, the RPi must have the bcm2835 library installed on it
