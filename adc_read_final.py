from ctypes import *
import ctypes
import numpy as np
from numpy.ctypeslib import ndpointer
import csv
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import datetime
import time
import sys
import random

CHANNELS = 8
initial_us = 0

so_file = "/home/pi/Documents/AD5592_Snack_Board/ad5592/ad5592_spi_read.so"
my_functions = CDLL(so_file)

def initialize_spi():
    global initial_us
    if(my_functions.initialize() == 0):
        print("Initialize Successful!\n")
    else:
        print("WARNING: Initialize Failed")
        sys.exit()  
    global duration
    duration = input("Enter sample duration (type 'r' for inifinite):")
    writer = csv.writer(file)
    writer.writerow(["Time (us)", "Signal 0", "Signal 1", "Signal 2", "Signal 3", "Signal 4", "Signal 5", "Signal 6", "Signal 7"])
    time.sleep(.1)
    initial_us = get_us()
    print(initial_us)

def get_us():
    now = datetime.datetime.now()
    return (now.minute*60000000)+(now.second*1000000)+(now.microsecond)
    
def get_elapsed_us():
    temp = get_us()
    return temp - initial_us

def find_position(code):
    if code == [1, 0, 1]:
        return 1
    if code == [0, 0, 1]:
        return 2
    if code == [0, 1, 1]:
        return 3
    if code == [0, 1, 0]:
        return 4
    if code == [1, 1, 0]:
        return 5
    if code == [1, 0, 0]:
        return 6
    if code == [0, 0, 0]:
        return 0

#def rising_edge_detect(data_new, data_old):

def read_spi(i, ys0, ys1, ys2, ys3, ys4, ys5, ys6, ys7):
    temp_data = np.uint32([0,0,0,0,0,0,0,0,0])
    old_data = np.uint32([0,0,0,0,0,0,0,0,0])
    for i in range(0, CHANNELS):
        temp_data[i+1] = my_functions.getAnalogIn(i)
    temp_data[0] = get_elapsed_us()
    writer = csv.writer(file)
    writer.writerow(temp_data)
    #print(temp_data)
    
    #rising_edge_detect(temp_data, old_data)
    old_data = temp_data
    
    if(duration != 'r'):
        if(temp_data[0] >= int(duration)*1000000):
            sys.exit()
    

    ys0.append(temp_data[1])
    ys1.append(temp_data[2])
    ys2.append(temp_data[3])
    ys3.append(temp_data[4])
    ys4.append(temp_data[5])
    ys5.append(temp_data[6])
    ys6.append(temp_data[7])
    ys7.append(temp_data[8])
    
    ys0 = ys0[-x_len:]
    ys1 = ys1[-x_len:]
    ys2 = ys2[-x_len:]
    ys3 = ys3[-x_len:]
    ys4 = ys4[-x_len:]
    ys5 = ys5[-x_len:]
    ys6 = ys6[-x_len:]
    ys7 = ys7[-x_len:]
    
    line0.set_ydata(ys0)
    line1.set_ydata(ys1)
    line2.set_ydata(ys2)
    line3.set_ydata(ys3)
    line4.set_ydata(ys4)
    line5.set_ydata(ys5)
    line6.set_ydata(ys6)
    line7.set_ydata(ys7)
    
    return line0,line1,line2,line3,line4,line5,line6,line7,
    
if __name__ == "__main__":
    initialize_spi()
    animation_ex()

