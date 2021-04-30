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

fig, axs = plt.subplots(4)
fig.suptitle('Motor Health')
plt.xlabel('Time (ms)')

CHANNELS = 8
initial_us = 0
pwm_target = 0
duration = 0
pwm_current = 0
position_cntr = 0

code_count = [[],[],[]]
last_position = 0
position_hold_time = 0
freq_count = [[],[]]


data = [[],[],[],[],[],[],[],[],[]]
data_single_revolution = [[],[],[],[]]

x = []
v = []
r = []
x_k_1 = 0.0
v_k_1 = 0.0
dt = 0.5 
alpha = 0.01
beta = .0001

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
        time.sleep(0.5)
    GPIO.output(motor_en, 0)
    graph_data()
    sys.exit()

def motor_shutdown():
    print("Starting shutdown...")
    pi_pwm.ChangeDutyCycle(0)
    GPIO.output(motor_en,0)
    graph_data()
    sys.exit()

def motor_reluctance(freq):
    temp_reluctance = freq/pwm_current
    return temp_reluctance

def get_rpm(position_hold_time):
    freq = (100000/((get_us() - position_hold_time)*6))
    freq_count[0].append(get_elapsed_us(initial_us))
    freq_count[1].append(freq)
    return freq

def health_check(temp_data):
    global last_position
    global position_hold_time
    global position_cntr
    code = [0,0,0]
    for i in range(1,4):
        if(temp_data[i] > 2500):
            code[i-1] = 1
        else:
            code[i-1] = 0
    position = find_position(code)
    if(last_position != position):
        if(last_position != 0):
            freq = get_rpm(position_hold_time)
            running_filter(freq)
            reluctance = motor_reluctance(x[-1])
            position_cntr = position_cntr + 1
            if(position_cntr == 6):
                rms_val = revolution_rms()
                position_cntr = 0
            else:
                rms_val = 0
            print("Elapsed: {}, ".format(get_elapsed_us(initial_us)) + "Position: {}, ".format(position) + "Frequency: {} ".format(round(freq, 2)) + "Filtered freq: {} ".format(x[-1]) +"PWM: {} ".format(pwm_current) + "Freq/PWM = {} ".format(reluctance) + "RMS Current: {}".format(rms_val))
        position_hold_time = get_us()
        last_position = position
    else:
        if((get_us() - position_hold_time) > 500000):
            print("****WARNING: STALL DETECTED****")
            motor_shutdown()

def running_filter(freq_data_current):
    global x
    global v
    global r
    global x_k_1
    global v_k_1

    x_k = x_k_1 + dt*v_k_1
    v_k = v_k_1
    r_k = freq_data_current - x_k
    x_k = x_k + alpha * r_k 
    v_k = v_k + (beta/dt)*r_k

    x_k_1 = x_k
    v_k_1 = v_k

    x.append(x_k)
    v.append(v_k)
    r.append(r_k)


def running_filter_time(freq_data_current):
    global x
    global v
    global r
    global x_k_1
    global v_k_1

    x_k = x_k_1 + dt*v_k_1
    v_k = v_k_1
    r_k = freq_data_current - x_k
    x_k = x_k + alpha * r_k 
    v_k = v_k + (beta/dt)*r_k

    x_k_1 = x_k
    v_k_1 = v_k

    x.append(x_k)
    v.append(v_k)
    r.append(r_k)       

def revolution_rms():
    return 0

def graph_data():
    #filter_data(freq_count[1])
    axs[0].plot(freq_count[0], x)
    axs[1].plot(data[4])
    axs[2].plot(data[5])
    axs[3].plot(data[6])
    plt.show()

def read_adc():
    global initial_us
    global position_hold_time
    global data
    global data_single_revolution
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
            if((pwm_counter % 1000) == 0):
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
            health_check(temp_data)
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