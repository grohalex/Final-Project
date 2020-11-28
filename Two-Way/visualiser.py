#lattice visualizer
import numpy as np
import scipy
import matplotlib as mpl
import matplotlib.pyplot as plt

"""
N = 10


fig, ax = plt.subplots()
#fig.set_size_inches(10,2)
ax.set_aspect(aspect=1)
"""

def lattice_grid(n,m,ax):
    #plot horizontal lines
    for i in range(m+1):
        ax.plot([0,n],[i,i], linestyle = '-', color = 'black')
    #plot vertical lines
    for i in range(n+1):
        ax.plot([i,i],[0,m],linestyle = '-', color = 'black')

#lattice: 0 = lattice 1, 1 = lattice 2
def lattice_points(ps,lattice,Color,ax):
    for i in ps:
        circle1 = plt.Circle((i+0.5, 0.5 + lattice), 0.45, color=Color)
        ax.add_artist(circle1)

#give out a vector with position of individual particles
def lattice2positions(lattice1, lattice2,ax):
    positions1_1 = np.array([])
    positions1_2 = np.array([])
    positions2_1 = np.array([])
    positions2_2 = np.array([])
    for i in range(len(lattice1)):
        if lattice1[i]==1:
            positions1_1 = np.append(positions1_1, i)
        if lattice1[i]==2:
            positions1_2 = np.append(positions1_2, i)

        if lattice2[i]==2:
            positions2_2 = np.append(positions2_2, i)
        elif lattice2[i]==1:
            positions2_1 = np.append(positions2_1, i)

    return positions1_1, positions1_2, positions2_2, positions2_1



"""
positions1_1, positions1_2, positions2_2, positions2_1 = lattice2positions([1,1,1,2,0,0,0,1], [2,2,2,0,0,0,0,1])

lattice_grid(10,2)
lattice_points(positions1_1, 0, "b")
lattice_points(positions1_2, 0, "r")
lattice_points(positions2_2, 1, "r")
lattice_points(positions2_1, 1, "b")
plt.show()
"""
