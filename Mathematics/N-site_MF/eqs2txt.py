#equations to txt: I want to produce a script for matlab which will produce all the equations into a txt file
import numpy as np
import random as random
import scipy
import matplotlib as mpl
import matplotlib.pyplot as plt

#pars: the only parameter is N (for how many sites we want to produce the equations)
N = 200
a = "a"
b = "b"



#save the matrix into a txt
Name = "equations_%s-site"%(N)
file1 = open(Name, "w")
heading = "%Nonlinear Equations for solving in MATLAB \n"

#######TEXT######
eq1 = "F(1) = %s*(1 - x(1)) - x(1)*(1 - x(2)) - x(1)*x(2)*(1 - y(2)); \n"%(a)
eq2 = "F(2) = x(1)*(1 - x(2)) - x(2)*(1 - x(3)) - x(2)*x(3)*(1 - y(3));\n"
file1.write(heading)
file1.write(eq1)
file1.write(eq2)

#writing the lattice1 densities equations:
I = 0
for i in range(3,N):
    print(i)###
    file1.write("F(%s) ="%i)
    file1.write("x(%s)*(1 - x(%s)) - x(%s)*(1 - x(%s)) + y(%s)*(1 - x(%s)) - x(%s)*x(%s)*(1 - y(%s));"%(i-1,i,i,i+1,i-1,i,i,i+1,i+1))
    file1.write("\n")
    I = i

    #last equation for densities in lattice1
eqN = "F(%s) =x(%s)*(1 - x(%s)) - %s*x(%s) + y(%s)*(1 - x(%s))  ;\n"%(I+1,N-1,N, b, N, N-1,N)
file1.write(eqN)
#writing the lattice2 densities equations:

    #eqN+1:
eqN1 = "F(%s) = x(1)*x(2)*(1 - y(2)) - y(2)*(1 - x(3)) - y(2)*x(3)*(1 - y(3))  ;\n"%(I+2)
file1.write(eqN1)


for j in range(I+3,2*N-1):
    i = j-I-2
    print(i)###
    file1.write("F(%s) ="%j)
    file1.write("x(%s)*x(%s)*(1 - y(%s)) - y(%s)*(1 - x(%s)) + y(%s)*x(%s)*(1 - y(%s)) - y(%s)*x(%s)*(1 - y(%s));"%(i+1,i+2,i+2,i+2,i+3,i+1,i+2,i+2,i+2,i+3,i+3))
    file1.write("\n")

eqNN = "F(%s) =x(%s)*x(%s)*(1 - y(%s)) - %s*y(%s) + x(%s)*y(%s)*(1 - y(%s)) ;\n" %(2*N-1,N-1,N,N,b,N,N,N-1,N)
file1.write(eqNN)



file1.close()
