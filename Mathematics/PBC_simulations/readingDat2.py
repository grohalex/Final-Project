#reading data.dat
import numpy as np
import numpy.random as rd
import random as random
import scipy
import matplotlib as mpl
import matplotlib.pyplot as plt

file1 = open("data2.dat",'r')
out2 = open("out2.txt", 'w')
data_string = []

#print(len(file1.readlines()))
#looping through the lines
for line in file1:
    if line[0:3]=='C22':
        print('yes')
        data_string = np.append(data_string, line[3:-1])
    else:
        print(line[0:3])

print(data_string)
data = np.zeros(len(data_string))
for i in range(len(data_string)):
    #data[i] = float(data_string[i])
    #out1.write(str(data[i]))
    out2.write(data_string[i])
    out2.write("\n")
