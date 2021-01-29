# first version of two way lattice stuck position heatmap
import numpy as np
import numpy.random as rd
import random as random
import scipy
import matplotlib as mpl
import matplotlib.pyplot as plt
from os import path
from datetime import datetime
now = datetime.now()

#parameters
N = 100     # number of sites
a1 = 1     # injection probability at lattice 1
a2 = 1     # injection probability at lattice 2
b1 = 1      # removal probability at lattice 1
b2 = 1      # removal probability at lattice 2
k11 = 1    # steping probability for particle 1 in lattice 1
#k12 = 0.1    # steping probability for particle 1 to lattice 2
#k21 = 0     # steping probability for particle 2 to lattice 1
k22 = 0.1     # steping probability for particle 2 in lattice 2

k12_values = [round(i, 2) for i in np.linspace(0,1,11)]#np.linspace(0,1,11)
k21_values = np.flip(k12_values)#[round(i, 2) for i in np.linspace(0,1,11)]
stuck_steps_matrix = np.zeros([ len(k21_values), len(k12_values)]) #init our heat maps
max_step = 600
averages = 5
#init
L1 = np.zeros(N)    #initialize lattice 1
L2 = np.zeros(N)    #initialize lattice 2
step = 0            #init step variable
#init the current measurement variables 'passed_particles'
passed_particles1 = 0  #particles which passes 0th site in latice 1
passed_particles2 = 0  #particles which passed 0th site in latice 2
current1 = 0
current2 = 0

densities1 = np.zeros(N) #average occupation density for each site in lattice 1
densities2 = np.zeros(N) #average occupation density for each site in lattice 2
#densities_a1 = np.zeros(steps_a) # densities corresponding to different initial a

#update ftion
def update(i):
    global passed_particles1,passed_particles2
    #insertion a1
    if i==0:
        if L1[0]==0 and rd.rand()<a1:
            L1[0]=1
            passed_particles1 +=1
    #in case there site = 1 there is particle 2 which should leave
    elif i==1 and L1[0]==2 and rd.rand()<b2: #in case there is particle 2 it leaves
        L1[0]=0

    #insertion a2
    elif i==N+1:
        if L2[0]==0 and rd.rand()<a2:
            L2[0]=2
            passed_particles2 +=1
    #in case site = 2N+1 and there is particle 1 it leaves
    elif i==N+2 and L2[0]==1 and rd.rand()<b2: #in case there is particle 1 it leaves
        L2[0]=0

    #removal b1
    elif i==N and rd.rand()<b1:
        if L1[-1]>0:
            L1[-1]=0

    #removal b2
    elif i==2*N+1 and rd.rand()<b2:
        if L2[-1]>0:
            L2[-1]=0


    #regular site lattice 1
    elif i>0 and i < N:
        i = i-1
        #update particle 1
        if L1[i]==1:
            #make a step
            if L1[i+1]==0 and rd.rand()<k11:
                L1[i]=0
                L1[i+1]=1

            #overtake
            elif L1[i+1]>0 and L2[-i-2]==0 and rd.rand()<k12:
                L1[i]=0
                L2[-i-2]=1

        #update particle 2
        if L1[i]==2:

            #finish overtaking
            if L2[-i]==0 and rd.rand()<k21:
                L1[i]=0
                L2[-i]=2
                if i == int(N/2):           ###
                    passed_particles1 +=1   ### #adding to the current in the second lattice (super coarse)


            #continue in the opposite lane
            elif L1[i-1]==0 and rd.rand()<k21:
                L1[i]=0
                L1[i-1]=2
                if i == int(N/2):           ###
                    passed_particles1 +=1   ### #adding to the current in the second lattice (super coarse)

    #regular site lattice 2
    elif i>N and i<2*N+1:
        i = i-N-2
        assert(i>=0 and i<=N)

        #update particle 2
        if L2[i]==2:
            #make a step
            if L2[i+1]==0 and rd.rand()<k22:
                L2[i]=0
                L2[i+1]=2

            #overtake
            elif L2[i+1]>0 and L1[-i-2]==0 and rd.rand()<k21:
                L2[i]=0
                L1[-i-2]=2

        #update particle 1
        if L2[i]==1:
            #finish overtaking
            if L1[-i]==0 and rd.rand()<k12:
                L2[i]=0
                L1[-i]=1
                if i == int(N/2):           ###
                    passed_particles2 +=1   ### #adding to the current in the second lattice (super coarse)


            #continue in the opposite lane
            elif L2[i-1]==0 and rd.rand()<k12:
                if not i==0:
                    L2[i]=0
                    L2[i-1]=1

                    if i == int(N/2):           ###
                        passed_particles2 +=1   ### #adding to the current in the second lattice (super coarse)


#lets you update the lattice with optional parameters. This is useful in the Stuck_position()
def update_par(i, A1, A2, B1, B2, K11, K22, K12, K21):

    #insertion a1
    if i==0:
        if L1[0]==0 and rd.rand()<A1:
            L1[0]=1
            return 1
        else:
            return 0
    #in case there site = 1 there is particle 2 which should leave
    elif i==1 and L1[0]==2 and rd.rand()<B2: #in case there is particle 2 it leaves
        L1[0]=0
        return 1
    #insertion a2
    elif i==N+1:
        if L2[0]==0 and rd.rand()<A2:
            L2[0]=2
            return 1
        else:
            return 0
    #in case site = 2N+1 and there is particle 1 it leaves
    elif i==N+2 and L2[0]==1 and rd.rand()<B2: #in case there is particle 1 it leaves
        L2[0]=0
        return 1
    #removal b1
    elif i==N and rd.rand()<B1:
        if L1[-1]>0:
            L1[-1]=0
            return 1
        else:
            return 0
    #removal b2
    elif i==2*N+1 and rd.rand()<B1:
        if L2[-1]>0:
            L2[-1]=0
            return 1
        else:
            return 0

    #regular site lattice 1
    elif i>0 and i < N:
        i = i-1

        if L1[i]==0: #nothing can change with no particle available
            return 0

        #update particle 1
        if L1[i]==1:
            #make a step
            if L1[i+1]==0 and rd.rand()<K11:
                L1[i]=0
                L1[i+1]=1
                return 1

            #overtake
            elif L1[i+1]>0 and L2[-i-2]==0 and rd.rand()<K12:
                L1[i]=0
                L2[-i-2]=1

                return 1
            else:
                return 0
        #update particle 2
        if L1[i]==2:

            if L2[i]==0: #nothing can change with no particle available
                return 0

            #finish overtaking
            if L2[-i]==0 and rd.rand()<K21:
                L1[i]=0
                L2[-i]=2
                return 1

            #continue in the opposite lane
            elif L1[i-1]==0 and rd.rand()<K21:
                L1[i]=0
                L1[i-1]=2
                return 1
            else:
                return 0



    #regular site lattice 2
    elif i>N:
        i = i-N-2
        assert(i>=0 and i<=N)

        #update particle 2
        if L2[i]==2:
            #make a step
            if L2[i+1]==0 and rd.rand()<K22:
                L2[i]=0
                L2[i+1]=2
                return 1
            #overtake
            elif L2[i+1]>0 and L1[-i-2]==0 and rd.rand()<K21:
                L2[i]=0
                L1[-i-2]=2
                return 1
            else:
                return 0
        #update particle 1
        elif L2[i]==1:
            #finish overtaking
            if L1[-i]==0 and rd.rand()<K12:
                L2[i]=0
                L1[-i]=1
                return 1
            #continue in the opposite lane
            elif L2[i-1]==0 and rd.rand()<K12:
                if not i==0:
                    L2[i]=0
                    L2[i-1]=1
                    return 1
            else:
                return 0
        else:
            return 0
    else:
        return 0

#does not update the lattice but it just outputs bool whether a move is possible. This is useful in the Stuck_position()
def update_bool(i, A1, A2, B1, B2, K11, K22, K12, K21):

    #insertion a1
    if i==0:
        if L1[0]==0 and rd.rand()<A1:
            #L1[0]=1
            return 1
        else:
            return 0
    #in case there site = 1 there is particle 2 which should leave
    elif i==1 and L1[0]==2 and rd.rand()<B2: #in case there is particle 2 it leaves
        #L1[0]=0
        return 1
    #insertion a2
    elif i==N+1:
        if L2[0]==0 and rd.rand()<A2:
            #L2[0]=2
            return 1
        else:
            return 0
    #in case site = 2N+1 and there is particle 1 it leaves
    elif i==N+2 and L2[0]==1 and rd.rand()<B2: #in case there is particle 1 it leaves
        #L2[0]=0
        return 1
    #removal b1
    elif i==N and rd.rand()<B1:
        if L1[-1]>0:
            #L1[-1]=0
            return 1
        else:
            return 0
    #removal b2
    elif i==2*N+1 and rd.rand()<B1:
        if L2[-1]>0:
            #L2[-1]=0
            return 1
        else:
            return 0

    #regular site lattice 1
    elif i>0 and i < N:
        i = i-1

        if L1[i]==0: #nothing can change with no particle available
            return 0

        #update particle 1
        if L1[i]==1:
            #make a step
            if L1[i+1]==0 and rd.rand()<K11:
                #L1[i]=0
                #L1[i+1]=1
                return 1

            #overtake
            elif L1[i+1]>0 and L2[-i-2]==0 and rd.rand()<K12:
                #L1[i]=0
                #L2[-i-2]=1

                return 1
            else:
                return 0
        #update particle 2
        if L1[i]==2:

            if L2[i]==0: #nothing can change with no particle available
                return 0

            #finish overtaking
            if L2[-i]==0 and rd.rand()<K21:
                #L1[i]=0
                #L2[-i]=2
                return 1

            #continue in the opposite lane
            elif L1[i-1]==0 and rd.rand()<K21:
                #L1[i]=0
                #L1[i-1]=2
                return 1
            else:
                return 0



    #regular site lattice 2
    elif i>N:
        i = i-N-2
        assert(i>=0 and i<=N)

        #update particle 2
        if L2[i]==2:
            #make a step
            if L2[i+1]==0 and rd.rand()<K22:
                #L2[i]=0
                #L2[i+1]=2
                return 1
            #overtake
            elif L2[i+1]>0 and L1[-i-2]==0 and rd.rand()<K21:
                #L2[i]=0
                #L1[-i-2]=2
                return 1
            else:
                return 0
        #update particle 1
        elif L2[i]==1:
            #finish overtaking
            if L1[-i]==0 and rd.rand()<K12:
                #L2[i]=0
                #L1[-i]=1
                return 1
            #continue in the opposite lane
            elif L2[i-1]==0 and rd.rand()<K12:
                if not i==0:
                    #L2[i]=0
                    #L2[i-1]=1
                    return 1
            else:
                return 0
        else:
            return 0
    else:
        return 0

#display both lattices, in the correct orientation
def Display():
    l1 = L1
    l2 = np.flip(L2) #L2 goes in the opposite direction

    print(l1)
    print(l2)

#another way of displaying my two lattices
def DisplayNice():
    l1 = L1
    l2 = np.flip(L2) #L2 goes in the opposite direction

    for i in l1:
        print('|', end = '')
        if i==1:
            print('o>', end = '')
        if i==2:
            print('<o', end = '')
        elif i==0:
            print('  ', end = '')
        #print('|', end = '')
    print('|', end = '')
    print('\n')

    for i in l2:
        print('|', end = '')
        if i==1:
            print('o>', end = '')
        if i==2:
            print('<o', end = '')
        elif i==0:
            print('  ', end = '')
        #print('|', end = '')
    print('|', end = '')
    print('\n')

#determines whether lattice is in a stuck position, returns a bool, True=lattice is stuck
def stuck_position():
    unstuck = 0
    for i in range(2*N+2):
        unstuck = unstuck + update_bool(i, 1,1,1,1,1,1,1,1)
    if unstuck > 0:
        return False
    if unstuck == 0:
        return True

    #this checks whether the update_par returns None (that would be an error)
#while True:
#    site = rd.randint(0,2*N+2)
#    if update_par(site, 1,1,1,1,1,1,1,1)==None:
#        print('omg no')

###########################################################################

for i in range(averages):
    #changing k12:
    for ii in range(len(k12_values)):
        k12 = k12_values[ii]
        print(k12)
        for jj in range(len(k21_values)):
            k21 = k21_values[jj]

            #I should empty the lattice here
            L1 = np.zeros(N)    #initialize lattice 1
            L2 = np.zeros(N)    #initialize lattice 2
            step = 0            #init step variable

            while not stuck_position() and not step > max_step:
                #print('yes')
                step += 1
                for j in range(2*N+2):
                    site = rd.randint(0,2*N+2)
                    update(site)
            print("step:", step)
            stuck_steps_matrix[jj,ii] += step/averages


#save the matrix into a txt
Name = "stuck_heatmapN%s"%(N)
heading = "parameters step: %s k12_values: %s \n k21_values %s \n"% (len(k12_values), k12_values, k21_values)
data = stuck_steps_matrix
data = np.array(data)
#data = np.transpose(data)
#fmt = "%-10d", "%-10.3f", "%-10.3f"
np.savetxt(Name, data, fmt = "%-10d", delimiter = "\t", header = heading)




#heat map plot:
f1 = plt.figure()
plt.xticks(ticks=np.arange(len(k12_values)),labels=k12_values)
plt.yticks(ticks=np.arange(len(k21_values)),labels=k21_values)
plt.title("Stuck Lattice heatmap(number of sites = %s, resolution in a = %s, b = %s)"%(N, len(k12_values), len(k21_values)))
plt.ylabel("k21 value")
plt.xlabel("k12 value")
# save this plot inside a variable called hm
hm=plt.imshow(stuck_steps_matrix, cmap='hot',interpolation="None")
# pass this heatmap object into plt.colorbar method.
plt.colorbar(hm)
plt.show()
