# first version of lattice TASEP
import numpy as np
import numpy.random as rd
import random as random
import scipy
import matplotlib as mpl
import matplotlib.pyplot as plt


#parameters
N = 100     # number of sites
a = 0.2      # injection probability
b = 1     # removal probability
k = 1       # steping probability
#steps = 200000       #steps
steady_state = 10000 #10000    #after the transient phase
sample_steps = [15000, 20000, 25000, 30000,35000, 40000]

#init
lattice = np.zeros(N)
passed_particles0 = 0           # passed_particles0 converges to the average current from above
#passed_particlesN = 0           # passed_particlesN converges to the average corrent from below
current = 0
densities = np.zeros(N)
std = np.zeros(len(sample_steps))



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
            #passed_particlesN += 1
    else:
        L_1 = Lattice[i-1]*Lattice[i]
        L_2 = Lattice[i]+(1-Lattice[i])*Lattice[i-1]
        Lattice[i-1] = L_1                       #otherwise I'd rewrite the Lattice
        Lattice[i] = L_2                         #before computing the next guy


    #return Lattice - no need to return anything

###########################################################################
for k in range(len(sample_steps)):
    steps = sample_steps[k]

    for i in range(steps):
        #print(i)
        for j in range(N+1):
            update(rd.randint(0,len(lattice)+1),lattice, a, b, k)
            #print(lattice)
            #update densities

            #if j<N:
                #densities[j] += lattice[j]/(steps)        #add only a weighted part of the density
        if i==steady_state:
            passed_particles0 = 0

        if i>=steady_state:              #we want to start measuring

            for j in range(N):
                densities[j] += lattice[j]/(steps-steady_state)
        #if i>=1 and i>steady_state:
            #current = (passed_particles0/2 + passed_particlesN/2)/i    #finding the avarage current (0 and N are there only to converge faster)
            #current = passed_particles0/i I don't need temporary current
            #print("cur: ",str(current), "\t pas0: ", str(passed_particles0/i), "\t pasN: ", str(passed_particlesN/i)  )
    #current = passed_particles0/(steps-steady_state)
    std[k] = np.std(densities[0:80])
    densities = np.zeros(N) #start measuring again
    lattice = np.zeros(N)   #start the simulation again (comment to start from populated lattice) ###

print(std)
#print(current)

#plot the standard deviations:
plt.plot(sample_steps,std,linestyle = '-', color = 'black', label = 'st. deviations', marker = 'o')
plt.title("Change in standart deviation of densities")
plt.xlabel('chosen steps number')
plt.ylabel('st. deviation')
plt.show()

'''
#save the density profile into a txt
Name = "density_profileN%sa%sb%s"%(N,a,b)
heading = "site \t DENSITY"
sites = np.arange(N)
data = sites,densities
data = np.array(data)
data = np.transpose(data)
fmt = "%-10d", "%-10.3f"
np.savetxt(Name, data, fmt = fmt, delimiter = "\t", header = heading)





print(densities)#
#plotting the density profile
fig,ax = plt.subplots()
ax.plot(range(len(densities)), densities, linestyle = '-', color = 'red', label = 'simulation')

props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
# place a text box in upper left in axes coords
ax.text(0.05, 0.15, "Current = %s"%round(current,3), transform=ax.transAxes, fontsize=14,
        verticalalignment='top', bbox=props)

Title = "Density profile of lattice with %s sites, a = %s, b = %s , steps = %s  "%(N,a,b, steps)
ax.set_title(Title)
ax.set_xlabel("ith position in the open lattice")
ax.set_ylabel("Average Site Occupancy (Density)")
plt.show()
'''
