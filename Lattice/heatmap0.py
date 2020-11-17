# producing a heat map script 0
import numpy as np
import numpy.random as rd
import random as random
import scipy
import matplotlib as mpl
import matplotlib.pyplot as plt

#first, just try a heatmap
'''
import matplotlib.pyplot as plt
medals = np.array([ [1,20,7],
                    [15,0,4],
                    [0, 25, 45]])

sports=['Football','Hockey','Tennis']
nations=['Czech','French','American']

plt.xticks(ticks=np.arange(len(sports)),labels=sports,rotation=90)
plt.yticks(ticks=np.arange(len(nations)),labels=nations)
# save this plot inside a variable called hm
hm=plt.imshow(medals, cmap='Blues',interpolation="nearest")
# pass this heatmap object into plt.colorbar method.
plt.colorbar(hm)
plt.show()

'''


#parameters
N = 100     # number of sites
a = 1      # injection probability
b = 1     # removal probability
k = 1       # steping probability
steps = 25000      #steps
steady_state = 10000 #10000    #after the transient phase
alphas = np.linspace(0,1,40) #the different rates we will look at
betas = np.flip(alphas)

#init
lattice = np.zeros(N)
passed_particles0 = 0           # passed_particles0 converges to the average current from above
#passed_particlesN = 0           # passed_particlesN converges to the average corrent from below
current = 0
densities = np.zeros(N)
current_a_b = np.zeros([ len(betas), len(alphas)]) #init our heat maps
density_a_b = np.zeros([ len(betas), len(alphas)])



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
for alpha in range(len(alphas)):
    for beta in range(len(betas)):
        lattice = np.zeros(N) #I start from an empty lattice
        passed_particles0 = 0 # I zero the
        densities = np.zeros(N)
        print("alpha: ", alphas[alpha], "beta: ", betas[beta] )

        #for each beta we simulate the entire system the number of steps
        for i in range(steps):
            #print(i)
            for j in range(N+1):
                update(rd.randint(0,len(lattice)+1),lattice, alphas[alpha], betas[beta], k)
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
        current_a_b[beta, alpha] = passed_particles0/(steps-steady_state)   #fill in a heatmap of currents at a,b
        density_a_b[beta, alpha] = np.average(densities)                    #fill in the heatmap for densities


#print(current)

#heat map plot:
f1 = plt.figure(1)
plt.xticks(ticks=np.arange(len(alphas)),labels=alphas,)
plt.yticks(ticks=np.arange(len(betas)),labels=betas)
plt.title("Average Current heatmap(number of sites = %s, resolution in a = %s, b = %s)"%(N, len(alphas), len(betas)))
# save this plot inside a variable called hm
hm=plt.imshow(current_a_b, cmap='hot',interpolation="None")
# pass this heatmap object into plt.colorbar method.
plt.colorbar(hm)

f2 = plt.figure(2)
plt.xticks(ticks=np.arange(len(alphas)),labels=[round(i,1) for i in alphas])
plt.yticks(ticks=np.arange(len(betas)),labels=[round(i,1) for i in betas])
plt.title("Average Density heatmap(number of sites = %s, resolution in a = %s, b = %s)"%(N, len(alphas), len(betas)))
# save this plot inside a variable called hm
hm=plt.imshow(density_a_b, cmap='hot',interpolation="None")
# pass this heatmap object into plt.colorbar method.
plt.colorbar(hm)
plt.show()


#save the matrix into a txt
Name = "heatmap_densityN%s"%(N)
heading = "Steps: %s cutoff: %s \n alphas: %s \n betas: %s \n"% (steps, steady_state, alphas, betas)
data = density_a_b
data = np.array(data)
#data = np.transpose(data)
np.savetxt(Name, data, fmt = "%-10.3f", delimiter = "\t", header = heading)

#save the matrix into a txt
Name = "heatmap_currentN%s"%(N)
heading = "Steps: %s cutoff: %s \n alphas: %s \n betas: %s \n"% (steps, steady_state, alphas, betas)
data = current_a_b
data = np.array(data)
#data = np.transpose(data)
np.savetxt(Name, data, fmt = "%-10.3f", delimiter = "\t", header = heading)

'''
#plotting the density profile
fig,ax = plt.subplots()
ax.plot(range(len(densities)), densities, linestyle = '-', color = 'red', label = 'simulation')

props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
# place a text box in upper left in axes coords
ax.text(0.05, 0.15, "Current = %s"%round(current,3), transform=ax.transAxes, fontsize=14,
        verticalalignment='top', bbox=props)
ax.set_ylim([0,1])
ax.set_xlim([0,100])
Title = "Density profile of lattice with %s sites, a = %s, b = %s , steps = %s  "%(N,a,b, steps)
ax.set_title(Title)
ax.set_xlabel("ith position in the open lattice")
ax.set_ylabel("Average Site Occupancy (Density)")
plt.show()
'''
