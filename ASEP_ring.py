#simulation of a simple ASEP Ring, confirming J = r(1-r) and max J, for different densities
import numpy as np
import numpy.random as rd
import random as random
import scipy
import matplotlib as mpl
import matplotlib.pyplot as plt

N = 100;        #number of sites of the ring
M = 10;         #number of particles in the ring
rate = 1;       #rate of moving (probability that the particle will move)
t_max = 100;    #how many time steps we will do

passed_particles = 0    #initialize


#ftion init_positions, populates ring in a random fashion
    #Ring1, Ind1 = init_positions(N,M) #how to call this ftion
def init_positions(n, m):
    ring = np.zeros(n)
    ind = list(range(n))
    indices = random.sample(ind, m)
    indices.sort() #this is not really needed

    for i in range(len(indices)):
        ring[indices[i]] = 1;

    return ring, indices

#Most Important:
#updates all the new positions according to the rules and also records the current
    # returns the updated ring and the current through the 0/1 boundary
def update_positions(ring, r, particles):
    for i in range(len(ring)):      #we loop through this random update n times (Monte Carlo)
        j = rd.randint(0,len(ring)) #choose j at random to update its position
        if j == len(ring)-1:        #if it is the last one: periodical conditions
            if ring[-1]>ring[0]:    #in case it is 1 and ring[0] is 0 the particle gets to the beginning
                ring[-1] = 0            #then we set last one to 0
                ring[0] = 1             #and the first one to 1

        elif ring[j]>ring[j+1]:     #if any position there is 1 followed by 0
            ring[j] = 0             #we move the particle
            ring[j+1] = 1
            if j == 0:
                particles = particles + 1 #and we also update the 'current'

    return ring, particles





####################################################



Ring, Ind = init_positions(N,M)
passed_particles = 0

for t in range(t_max):
    Ring, passed_particles = update_positions(Ring,rate, passed_particles)
    print(Ring)
    print(passed_particles)

average_current = passed_particles/t_max
print("avg current: ",average_current )
