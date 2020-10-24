import ASEP_ring as ASEP_ring

import numpy as np
import numpy.random as rd
import random as random
import scipy
import matplotlib as mpl
import matplotlib.pyplot as plt

from scipy.interpolate import interp1d
from scipy.signal import savgol_filter

#Generate plots of ASEP ring simulation
    #average_current = ASEP_ring.simulate(100,50,1,500)
#print(average_current)


N = 100
steps = 1000
rhos = np.arange(0,1+0.01,0.01)
ms = N*rhos
avg_currents = list(range(len(rhos)))
plot_title = 'ASEP Ring Simulation of N=' + str(N) +" "+ "sites with " + str(len(rhos)) + " density steps and t=[0, " + str(steps) + "]"


#mathematical model prediction
currents = list(range(len(rhos)))
for i in range(len(rhos)):
    currents[i] = rhos[i]*(1-rhos[i])

#simulation values
for i in range(len(ms)):
    avg_currents[i] = ASEP_ring.simulate(100,int(ms[i]),1,steps)
print(avg_currents)


#saving results into file
datafile = "avg-current_N%sS%s.txt"%(N,steps)
heading = "Density \t particles \t CURRENT"
data = rhos,ms,avg_currents     #add all the data into a large matrix
data = np.array(data)           #convert them to np.array
data = np.transpose(data)       #I need to transpose for the dimesion in txt file
fmt = "%-10.2f", "%-10d", "%-10.3f"    # I want to have a different number formt for each column
np.savetxt(datafile, data, fmt = fmt, delimiter = "\t", header = heading)
#fmt = formating text

#smoothed simulation values
    #interpolation
f = scipy.interpolate.interp1d(rhos, avg_currents, kind = 'linear')
rhos_interp = np.linspace(rhos[0], rhos[-1], 500)
y_interp = f(rhos_interp)
    #smoothing
window = 101
polynom = 3
y_smooth = savgol_filter(f(rhos_interp), window, polynom)


#plot different figures
plt.figure()
#plt.plot(rhos_interp, y_smooth, linestyle = '-', color = 'black', label = 'smoothed simulation')
plt.plot(rhos, avg_currents,linestyle = ':', marker ='o', color = 'black', label = 'simulation')
plt.plot(rhos, currents , color = 'blue', linestyle = '-', label = 'mathematical model prediction')
plt.title(plot_title)
plt.xlabel('density')
plt.ylabel('average current')
plt.legend()
plt.show()

#plot reference:
'''
plt.figure()
plt.plot(data[:,0], data[:,1], color = 'red', linestyle = 'dashed', marker = 'o', label = data_names[1])
#plotting x - month (first column), y - max. temperature(second column), +options, label is from list data_names
plt.plot(data[:,0], data[:,2]  ,color = 'blue', linestyle = 'dashed', marker = 's', label = data_names[2])

#adding decoration:
plt.title ("Temperature in Dyce by Month")
plt.legend()
plt.xlim(0,12)
plt.xlabel(data_names[0])
plt.ylabel("Temeprature in C")
plt.show()

plt.figure()
xs = np.arange(0,10,0.1)
ys = np.sin(xs)
ys2 = np.cos(xs)
plt.plot(xs,ys)
plt.plot(xs,ys2)

plt.show()
'''
