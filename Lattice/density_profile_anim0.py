# first version of lattice TASEP
import numpy as np
import numpy.random as rd
import random as random
import scipy
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import animation


#parameters
N = 100     # number of sites
a = 0.2      # injection probability
b = 0.2      # removal probability
k = 1       # steping probability
steps = 2000

#init
lattice = np.zeros(N)
passed_particles0 = 0           # passed_particles0 converges to the average current from above
passed_particlesN = 0           # passed_particlesN converges to the average corrent from below
current = 0
densities = np.zeros(N)
densities_evol = np.zeros((steps,N)) #for the animation



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
            densities[j] += lattice[j]/(steps)        #add only a weighted part of the density


    if i>=1:
        densities_evol[i] = densities*steps/i   #update each time step the density evolution
        current = (passed_particles0/2 + passed_particlesN/2)/i    #finding the avarage current (0 and N are there only to converge faster)
        #print("cur: ",str(current), "\t pas0: ", str(passed_particles0/i), "\t pasN: ", str(passed_particlesN/i)  )


#save the density profile into a txt
Name = "dens_prof_evol_N%sa%sb%s.txt"%(N,a,b)
heading = "site \t DENSITY"
data = densities_evol
np.savetxt(Name, data, fmt = "%1.2f", delimiter = " ", newline = "\n \n", header = "Densities in %s sites changing in %s time steps"%(N,steps))

#for i in range(steps):
    #print(densities_evol[i], '\n')



#animation
"""
author: Jake Vanderplas
email: vanderplas@astro.washington.edu
website: http://jakevdp.github.com
license: BSD
Please feel free to use and modify this, but keep the above information. Thanks!
"""

# First set up the figure, the axis, and the plot element we want to animate
fig = plt.figure()
ax = plt.axes(xlim=(0, 100), ylim=(0, 0.6))
Title = "Density profile of lattice with %s sites, a = %s, b = %s  "%(N,a,b)
ax.set_title(Title)
line, = ax.plot([], [], lw=2)
time_text = ax.text(0.05,0.95,"",transform = ax.transAxes)

# initialization function: plot the background of each frame
def init():
    line.set_data([], [])
    return line,

# animation function.  This is called sequentially
def animate(i):
    x = np.arange(N-1)
    y = densities_evol[i,x]
    line.set_data(x, y)
    time_text.set_text('time: '+ str(i))
    return line, time_text

# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=steps, interval=10, blit=True, repeat = False)

# save the animation as an mp4.  This requires ffmpeg or mencoder to be
# installed.  The extra_args ensure that the x264 codec is used, so that
# the video can be embedded in html5.  You may need to adjust this for
# your system: for more information, see
# http://matplotlib.sourceforge.net/api/animation_api.html
anim.save('dens_prof_animation%s.gif'%steps, fps=30, extra_args=['-vcodec', 'libx264'])

plt.show()
