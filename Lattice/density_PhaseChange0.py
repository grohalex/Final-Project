# first version of lattice TASEP
import numpy as np
import numpy.random as rd
import random as random
import scipy
import matplotlib as mpl
import matplotlib.pyplot as plt


#parameters
N = 100         # number of sites
a = 0           # injection probability
b = 0.9        # removal probability
k = 1           # steping probability
steps = 2000

da = 0.025       # step in a
steps_a = int(1/da)  # how many simulations we will run with different a's
As = np.arange(0,1, da) # all a's that I will simulate for


#init
lattice = np.zeros(N)
passed_particles0 = 0           # passed_particles0 converges to the average current from above
passed_particlesN = 0           # passed_particlesN converges to the average corrent from below
current = 0
densities = np.zeros(N)
densities_a = np.zeros(steps_a) # densities corresponding to different initial a


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

for k in range(len(densities_a)):
    a = As[k]                           #update a new value for a
    print(k ,". a:" , str(a)) ###
    densities = np.zeros(N)     # I will zero it for each a
    for i in range(steps):
        for j in range(N+1):
            update(rd.randint(0,len(lattice)+1),lattice, a, b, k)
            #print(lattice)
            #update densities
            if j<N:
                densities[j] += lattice[j]/(steps)        #add only a weighted part of the density

        if i>=1:
            current = (passed_particles0/2 + passed_particlesN/2)/i    #finding the avarage current (0 and N are there only to converge faster)
            #print("cur: ",str(current), "\t pas0: ", str(passed_particles0/i), "\t pasN: ", str(passed_particlesN/i)  )

    densities_a[k] = np.average(densities)
    #if k==0:
    #    densities_a[k] = np.average(densities)
    #else:
    #    densities_a[k] = np.average(densities)/k

print(densities)
print(densities_a)


#save the phase transition of densities into a txt
Name = "phaseTransitionN%sb%s"%(N,b)
heading = "value of a \t DENSITY"
data = As,densities_a
data = np.array(data)
data = np.transpose(data)
fmt = "%-10.2f", "%-10.3f"
np.savetxt(Name, data, fmt = fmt, delimiter = "\t", header = heading)






#plotting the phase transition
fig,ax = plt.subplots()
ax.plot(As, densities_a, linestyle = '-', color = 'red', label = 'simulation')

Title = "Phase transition in a lattice with %s sites, b = %s and changing a, steps/a = %s  "%(N,b, steps)
ax.set_title(Title)
ax.set_xlabel("value of a")
ax.set_ylabel("Average Density")
plt.show()
