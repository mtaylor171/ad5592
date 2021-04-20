from ctypes import *
import ctypes
import numpy as np
from numpy.ctypeslib import ndpointer
import csv
import matplotlib.pyplot as plt
import datetime
import time
import sys
import random
import RPi.GPIO as GPIO

ACTIVE_CHANNELS = 8

x_len = 200
y_range = [0, 3500]

filename = str(datetime.datetime.now())
file = open(filename, 'w', newline='')

motor_en = 15
pwmpin = 32             # PWM pin connected to LED
GPIO.setwarnings(False)         #disable warnings
GPIO.setmode(GPIO.BOARD)        #set pin numbering system
GPIO.setup(pwmpin,GPIO.OUT)
pi_pwm = GPIO.PWM(pwmpin,25000)      #create PWM instance with frequency
GPIO.setup(motor_en, GPIO.OUT)

plt.title('ADC Data')
plt.xlabel('Time (ms)')
plt.ylabel('Signal')

CHANNELS = 8
initial_us = 0
pwm_target = 0
duration = 0
pwm_current = 0

code_count = [[],[],[]]
last_position = 0
position_hold_time = 0
freq_count = []


data = [[],[],[],[],[],[],[],[], []]

so_file = "/home/pi/Documents/motor_board/ad5592/ad5592_spi_read.so"
my_functions = CDLL(so_file)

def initialize_spi():
    global initial_us
    GPIO.output(motor_en, 1)
    if(my_functions.initialize_motor() == 0):
        print("Motor Initialize Successful!\n")
    else:
        print("WARNING: Initialize Failed")
        sys.exit()
    for i in range(0, 19):
        reg_data = my_functions.motor_register_read(i)
        print('Register {}:'.format(i) + ' {}'.format(hex(reg_data)));
        print('\n')
    reg_check = input("Are Registers correct? (y/n)")
    if(reg_check != 'y'):
        sys.exit()
    if(my_functions.initialize() == 0):
        print("ADC Initialize Successful!\n")
    else:
        print("WARNING: Initialize Failed")
        sys.exit()  

def get_us():
    now = datetime.datetime.now()
    return (now.minute*60000000)+(now.second*1000000)+(now.microsecond)
    
def get_elapsed_us(timestamp):
    temp = get_us()
    return (temp - timestamp)

def find_position(code):
    if code == [1, 0, 1]:
        return 1
    elif code == [0, 0, 1]:
        return 2
    elif code == [0, 1, 1]:
        return 3
    elif code == [0, 1, 0]:
        return 4
    elif code == [1, 1, 0]:
        return 5
    elif code == [1, 0, 0]:
        return 6
    else:
        return 0

#def rising_edge_detect(data_new, data_old):

def data_process(data):
    adc_reading = int((data & 0x0FFF) / 0.819)
    index = ((data >> 12) & 0x7)
    return adc_reading, index

def user_inputs():
    global duration
    global pwm_current
    global pwm_target
    duration = input("Enter sample duration (type 'r' for inifinite):")
    writer = csv.writer(file)
    writer.writerow(["Time (us)", "Signal 0", "Signal 1", "Signal 2", "Signal 3", "Signal 4", "Signal 5", "Signal 6", "Signal 7"])
    time.sleep(.1)
    pwm_target = input("Enter target duty cycle:")
    pwm_current = 0
    pi_pwm.start(pwm_current)
    
def pwm_control():
    global pwm_current
    if(pwm_current < int(pwm_target)):
        pwm_current = pwm_current + 1
        print("PWM: {}".format(pwm_current))
    pi_pwm.ChangeDutyCycle(pwm_current)             #start PWM of required Duty Cycle

def motor_rampdown():
    print("Starting rampdown...")
    for duty in range(pwm_current,-1,-1):
        pi_pwm.ChangeDutyCycle(duty)
        print("PWM: {}".format(duty))
        time.sleep(0.1)
    GPIO.output(motor_en, 0)
    graph_data()
    sys.exit()

def motor_shutdown():
    print("Starting shutdown...")
    pi_pwm.ChangeDutyCycle(0)
    GPIO.output(motor_en,0)
    sys.exit()

def get_rpm(position_hold_time):
    freq = (1000000/(get_us() - position_hold_time))/6
    freq_count.append(freq)
    return freq

def stall_check(temp_data):
    global last_position
    global position_hold_time
    code = [0,0,0]
    for i in range(1,4):
        if(temp_data[i] > 2500):
            code[i-1] = 1
        else:
            code[i-1] = 0
    position = find_position(code)
    if(last_position != position):
        freq = get_rpm(position_hold_time)
        print("Position: {}".format(position) + "Frequency: {}".format(freq))
        position_hold_time = get_us()
        last_position = position
    else:
        if((get_us() - position_hold_time) > 500000):
            print("****WARNING: STALL DETECTED****")
            motor_shutdown()

def graph_data():
    plt.plot(freq_count)
    plt.show()

def read_adc():
    global initial_us
    global position_hold_time
    global data
    temp_data = np.uint32([0,0,0,0,0,0,0,0,0])
    adc_reading = 0x0
    index = 0x0
    dat_16bit = 0x0
    pwm_counter = 0
    initial_us = get_us()
    my_functions.getAnalogInAll_InitialSend()
    position_hold_time = get_us()
    while(1):
        try:
            if((pwm_counter % 50) == 0):
                pwm_control()
            pwm_counter = pwm_counter + 1
            for i in range(0, ACTIVE_CHANNELS):
                data_16bit = my_functions.getAnalogInAll_Receive()
                adc_reading, index = data_process(data_16bit)
                temp_data[index+1] = adc_reading
                data[index+1].append(temp_data[index+1])
            temp_data[0] = get_elapsed_us(initial_us)
            data[0].append(temp_data[0])
            #print('Time Elapsed: {}'.format(temp_data[0]))
            writer = csv.writer(file)
            writer.writerow(temp_data)
            stall_check(temp_data)
            if(duration != 'r'):
                if(temp_data[0] >= int(duration) * 1000000):
                    my_functions.getAnalogInAll_Terminate()
                    motor_rampdown()
        except KeyboardInterrupt:
            my_functions.getAnalogInAll_Terminate()
            motor_rampdown()
    
if __name__ == "__main__":
    initialize_spi()
    user_inputs()
    read_adc()