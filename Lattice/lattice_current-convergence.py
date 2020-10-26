# first version of lattice TASEP
import numpy as np
import numpy.random as rd
import random as random
import scipy
import matplotlib as mpl
import matplotlib.pyplot as plt

#parameters
N = 100     # number of sites
a = 1      # injection probability
b = 1       # removal probability
k = 1       # steping probability
steps = 10000

#init
lattice = np.zeros(N)
passed_particles0 = 0           # passed_particles0 converges to the average current from above
passed_particlesN = 0           # passed_particlesN converges to the average corrent from below
current = 0

#convergence figures
currents_above = np.zeros(steps-1)
currents_below = np.zeros(steps-1)
currents = np.zeros(steps-1)



#ftion update looks at ith site and updates its and its neighbours value
def update(i,Lattice,A,B,K):
    global passed_particles0,passed_particlesN
    assert(i<=N)

    if i==0:
        if Lattice[0]==0 and rd.rand()<A:
            Lattice[0] = 1
            passed_particles0 += 1
    elif i==len(Lattice):
        if Lattice[-1]==1 and rd.rand()<B:
            Lattice[-1] = 0
            passed_particlesN += 1
    else:
        L_1 = Lattice[i-1]*Lattice[i]
        L_2 = Lattice[i]+(1-Lattice[i])*Lattice[i-1]
        Lattice[i-1] = L_1                       #otherwise I'd rewrite the Lattice
        Lattice[i] = L_2                         #before computing the next guy


    #return Lattice - no need to return anything

###########################################################################
print(len(lattice) == N)
for i in range(steps):
    for j in range(N+1):
        update(rd.randint(0,len(lattice)+1),lattice, a, b, k)
        #print(lattice)

    if i>=1:
        current = (passed_particles0/2 + passed_particlesN/2)/i    #finding the avarage current (0 and N are there only to converge faster)
        print("cur: ",str(current), "\t pas0: ", str(passed_particles0/i), "\t pasN: ", str(passed_particlesN/i)  )
        currents_above[i-1] = passed_particles0/i
        currents_below[i-1] = passed_particlesN/i
        currents[i-1] = current

#plotting
plt.figure()
plt.plot(range(len(currents)), currents ,linestyle = '-', color = 'red', label = 'Current average')
plt.plot(range(len(currents)), currents_above ,linestyle = '-', color = 'blue', label = 'Current at site 0')
plt.plot(range(len(currents)), currents_below ,linestyle = '-', color = 'black', label = 'Current at site N')
plt.ylim(0,0.5)
plt.title("Currents at the first and last position convergence")
plt.xlabel('step')
plt.ylabel('current')
plt.legend()
plt.show()
