import numpy as np
import matplotlib.pyplot as plt
import csv

import seaborn as sns
sns.set_style('whitegrid')
sns.set_context('poster')

time = []
y = []

def collect_data():
    with open(fileName, 'r') as csvfile:
        plots = csv.reader(csvfile,delimiter=',')
        next(plots)
        for row in plots:
            time.append(float(row[0]))
            y.append(float(row[1]))
    
fileName = input("Enter filename:")
collect_data()
meas = y

x = []
v = []
r = []
x_k_1 = 0.0
v_k_1 = 0.0
dt = 0.5 

alpha = 0.01
beta = .00005


for k in range(len(meas)):
	x_k = x_k_1 + dt*v_k_1
	v_k = v_k_1
	r_k = meas[k] - x_k
	x_k = x_k + alpha * r_k 
	v_k = v_k + (beta/dt)*r_k

	x_k_1 = x_k
	v_k_1 = v_k

	x.append(x_k)
	v.append(v_k)
	r.append(r_k)

fig, (ax1, ax2) = plt.subplots(2)
fig.suptitle(r'Alpha-Beta-Tracker: $\alpha$=%.2f und $\beta$=%.4f' % (alpha, beta))

ax1.plot(time, x, label=u'Estimated Position')
ax2.plot(time, meas, label=u'Position Measurement')
plt.xlabel('Time [s]')
ax1.set(ylabel = 'Motor Speed (rev/s)')
ax2.set(ylabel = 'Motor Speed (rev/s)')
ax1.legend(loc=4)
ax2.legend(loc=4)

plt.show()