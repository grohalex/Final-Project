# first version of lattice TASEP
import numpy as np
import numpy.random as rd
import random as random
import scipy
import matplotlib as mpl
import matplotlib.pyplot as plt

#parameters
N = 100     # number of sites
a = 0.5      # injection probability
b = 1       # removal probability
k = 1       # steping probability
steps = 30000

#init
lattice = np.zeros(N)
passed_particles0 = 0           # passed_particles0 converges to the average current from above
passed_particlesN = 0           # passed_particlesN converges to the average corrent from below
current = 0
densities = np.zeros(N)



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

for i in range(steps):
    for j in range(N+1):
        update(rd.randint(0,len(lattice)+1),lattice, a, b, k)
        #print(lattice)
        #update densities
        if j<N:
            densities[j] += lattice[j]/(steps*N)        #add only a weighted part of the density

    if i>=1:
        current = (passed_particles0/2 + passed_particlesN/2)/i    #finding the avarage current (0 and N are there only to converge faster)
        #print("cur: ",str(current), "\t pas0: ", str(passed_particles0/i), "\t pasN: ", str(passed_particlesN/i)  )

print(densities)###
fig,ax = plt.subplots()


ax.plot(range(len(densities)), densities, linestyle = '-', color = 'red', label = 'simulation')

props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
# place a text box in upper left in axes coords
ax.text(0.05, 0.15, "Current = %s"%round(current,3), transform=ax.transAxes, fontsize=14,
        verticalalignment='top', bbox=props)

Title = "Density profile of lattice with %s sites, a = %s, b = %s  "%(N,a,b)
ax.set_title(Title)
ax.set_xlabel("ith position in the open lattice")
ax.set_ylabel("Average Site Occupancy (Density)")
plt.show()
