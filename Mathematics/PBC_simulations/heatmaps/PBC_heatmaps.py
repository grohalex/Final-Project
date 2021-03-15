# first version of two way lattice for getting current
import numpy as np
import numpy.random as rd
import random as random
import scipy
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from datetime import datetime
now = datetime.now()

#parameters
N = 100     # number of sites
rho_t = 1.3 #total fraction of particles in the system -> from 0 (empty) to 2 (both lattices are full)
M = int(rho_t*N) #absolute number of particles in the system (rho_t goes up to 2 because if N=10, max number of particles is 20)

K12_1 = linspace(0.0,1,10)    # steping probability for particle 1 to lattice 2
K21_1 = linspace(0.0,1,10)#0     # steping probability for particle 1 to lattice 1
k11_1 = 1     # steping probability for particle 1 in lattice 1
k12_1 = 0    # steping probability for particle 1 to lattice 2
k21_1 = 0#0     # steping probability for particle 1 to lattice 1
k22_1 = 1#0     # steping probability for particle 1 in lattice 2
k11_2 = 0     # steping probability for particle 2 in lattice 1
k12_2 = 0#0.2    # steping probability for particle 2 to lattice 2
k21_2 = 0#0     # steping probability for particle 2 to lattice 1
k22_2 = 0#0     # steping probability for particle 2 in lattice 2

steps = 20000           #total steps
steady_state = 10000    #after the transient phase (we start measuring)

#init
L1 = np.zeros(N)    #initialize lattice 1
L2 = np.zeros(N)    #initialize lattice 2
    #init the current measurement variables 'passed_particles'
passed_particles1 = 0  #particles which passes 0th site in latice 1
passed_particles2 = 0  #particles which passed 0th site in latice 2
current1 = 0
current2 = 0
avg_density1 = 0    #avg_density in lattice 1
avg_density2 = 0    #avg_density in lattice 2
densities1 = np.zeros(N) #average occupation density for each site in lattice 1
densities2 = np.zeros(N) #average occupation density for each site in lattice 2
density_matrix1 = np.zeros([len(A1),len(A1)])# a heatmap recording the avg densities in lattice 1
density_matrix2 = np.zeros([len(A1),len(A1)])# a heatmap recording the avg densities in lattice 2
current_matrix1 = np.zeros([len(A1),len(A1)])# a heatmap recording the avg densities in lattice 1
current_matrix2 = np.zeros([len(A1),len(A1)])# a heatmap recording the avg densities in lattice 2
current_total =np.zeros([len(A1),len(A1)])  #total current through the lattice
#densities_a1 = np.zeros(steps_a) # densities corresponding to different initial a

#update ftion
def update(i):
    global passed_particles11,passed_particles12, passed_particles21,passed_particles22
    #insertion a1 - no insertion in PBC!
    if i==0:
        if L1[0]==1 and L1[1]==0 and rd.rand()<k11_1: #particle1 continues in L1
            L1[0]=0
            L1[1]=1
            passed_particles11 +=1

        elif L1[0]==1 and L1[1]>0 and L2[-2]==0 and rd.rand()<k11_1: #particle1 overtakes
            L1[0]=0
            L2[-2]=1
            passed_particles12 +=1

        elif L1[0]==2 and L2[0]==0 and rd.rand()<k12_2:     #particle2 goes into lane 2
            L1[0]=0
            L2[0]=2
            #passed_particles21 +=1

        elif L1[0]==2 and L2[0]>0 and L1[-1]==0 and rd.rand()<k11_2:    #particle2 continues in L1
            L1[0]=0
            L1[-1]=2
            #passed_particles21 +=1
    #in case there site = 1 there is particle 2 which should leave ------> not in PBC
    #elif i==1 and L1[0]==2 and rd.rand()<b2: #in case there is particle 2 it leaves
    #    L1[0]=0

    #insertion a2 - no insertion in PBC!!!
    elif i==N:
        if L2[0]==2 and L2[1]==0 and rd.rand()<k22_2: #particle2 continues in L2
            L2[0]=0
            L2[1]=2
            #passed_particles22 +=1

        elif L2[0]==2 and L2[1]>0 and L1[-2]==0 and rd.rand()<k21_2: #particle2 overtakes
            L2[0]=0
            L2[-2]=2
            #passed_particles22 +=1

        elif L2[0]==1 and L1[0]==0 and rd.rand()<k21_1:     #particle1 goes into lane 1
            L2[0]=0
            L1[0]=1
            passed_particles21 +=1


        elif L2[0]==1 and L1[0]>0 and L2[-1]==0 and rd.rand()<k22_1:    #particle1 continues in L2
            L2[0]=0
            L2[-1]=1
            passed_particles22 +=1

    #in case site = 2N+1 and there is particle 1 it leaves -----> not in PBC
    #elif i==N+2 and L2[0]==1 and rd.rand()<b2: #in case there is particle 1 it leaves
    #    L2[0]=0

    #periodic boundaries at L1[end]->L1[0] or L1[end]->L2[0]
    elif i==N-1:
        if L1[-1]==1 and L1[0]==0 and rd.rand()<k11_1: #it goes to the beginning again (PCB)
            L1[-1]=0
            L1[0]=1
        if L1[-1]==1 and L1[0]>0 and L2[-1]==0 and rd.rand()<k12_1:  #it overtakes into the 2nd line (PCB)
            L1[-1]=0
            L2[-1]=1
        if L1[-1]==2 and L2[1]==0 and rd.rand()<k12_2:    #particle 2 come back to lattice 2
            L1[-1]=0
            L2[1]=2
        if L1[-1]==2 and L2[1]>0 and L1[-2]==0 and rd.rand()<k11_2:    #particle 2 continue in the opposite lane
            L1[-1]=0
            L1[-2]=2

    #periodic boundaries at L2[end]->L2[0] or L2[end]->L1[0]
    elif i==2*N-1:
        #it goes to the beginning again (PCB)
        if L2[-1]==2 and L2[0]==0 and rd.rand()<k22_2: #it goes to the beginning again (PCB)
            L2[-1]=0
            L2[0]=2
        #it overtakes into the 1st line (PCB)
        if L2[-1]==2 and L2[0]>0 and L1[0]==0 and rd.rand()<k21_2:
            L2[-1]=0
            L1[0]=2
        #particle 1 comes back to lattice 1
        if L2[-1]==1 and L1[1]==0 and rd.rand()<k21_1:
            L2[-1]=0
            L1[1]=1
        #particle 1 continue in the opposite lane, lattice 2
        if L2[-1]==1 and L1[1]>0 and L2[-2]==0 and rd.rand()<k22_1:
            L2[-1]=0
            L2[-2]=1

    #regular site lattice 1
    elif i>0 and i < N:
        ###i = i-1
        #update particle 1
        if L1[i]==1:
            #make a step
            if L1[i+1]==0 and rd.rand()<k11_1:
                L1[i]=0
                L1[i+1]=1

            #overtake
            elif L1[i+1]>0 and L2[-i-2]==0 and rd.rand()<k12_1:
                L1[i]=0
                L2[-i-2]=1

        #update particle 2
        if L1[i]==2:

            #finish overtaking
            if L2[-i]==0 and rd.rand()<k12_2:
                L1[i]=0
                L2[-i]=2

            #continue in the opposite lane
            elif L1[i-1]==0 and rd.rand()<k11_2:
                L1[i]=0
                L1[i-1]=2

    #regular site lattice 2
    elif i>=N and i<=2*N-1:
        i = i-N
        assert(i>=0 and i<=N)

        #update particle 2
        if L2[i]==2:
            #make a step
            if L2[i+1]==0 and rd.rand()<k22_2:
                L2[i]=0
                L2[i+1]=2

            #overtake
            elif L2[i+1]>0 and L1[-i-2]==0 and rd.rand()<k21_2:
                L2[i]=0
                L1[-i-2]=2

        #update particle 1
        if L2[i]==1:
            #finish overtaking
            if L1[-i]==0 and rd.rand()<k21_1:
                L2[i]=0
                L1[-i]=1

            #continue in the opposite lane
            elif L2[i-1]==0 and rd.rand()<k22_1:
                if not i==0:
                    L2[i]=0
                    L2[i-1]=1



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

def init_positions_particles1(n, m):
    l1 = np.zeros(n)
    l2 = np.zeros(n)
    ind = list(range(2*n))

    #print(m)
    indices = random.sample(ind, m)
    indices.sort() #this is not really needed


    for i in range(len(indices)):
        if indices[i]<=N-1:
            l1[indices[i]] = 1;
        elif indices[i]>N-1:
            l2[indices[i]-N] = 1;


    return l1, l2
###########################################################################

#Working simulation:
'''
j = 0
while True:#j<100:
    print(j)
    site = int(input("ch: "))#rd.randint(0,2*N+2)
    #site = rd.randint(0,2*N+2)
    #print(site)
    #update(site)
    print(update_par(site, 1,1,1,1,1,1,1,1))
    print(stuck_position())
    DisplayNice()
    j+=1
'''
for step in range(len(K_12)):
    k12 = K_12[step]
    k21 = K_21[step]
    print("k12: ",k12, "\t k21: ", k21)

    C_total = np.zeros(len(M))  #total current
    C11 = np.zeros(len(M)) #current in l1 -> l1
    C12 = np.zeros(len(M)) #current in l1 -> l2
    C21 = np.zeros(len(M)) #current in l2 -> l1
    C22 = np.zeros(len(M)) #current in l2 -> l2
    for mm in range(len(M)):
        #init
        L1 = np.zeros(N)    #initialize lattice 1
        L2 = np.zeros(N)    #initialize lattice 2
        #init the current measurement variables 'passed_particles'
        passed_particles11 = 0  #particles which passes 0th site latice 1 -> lattice 1
        passed_particles12 = 0  #particles which passed 0th site lattice 1 -> lattice 2
        passed_particles21 = 0  #particles which passed 0th site lattice 2 -> lattice 1
        passed_particles22 = 0  #particles which passed 0th site lattice 2 -> lattice 2
        current11 = 0
        current12 = 0
        current21 = 0
        current22 = 0

        L1, L2 = init_positions_particles1(N,int(M[mm]))

        for i in range(steps):
            for j in range(2*N):
                site = rd.randint(0,2*N)
                update(site)
            #cutoff (steady state) period
            if i == steady_state: #we start measuring from 0
                    passed_particles11 = 0
                    passed_particles12 = 0
                    passed_particles21 = 0
                    passed_particles22 = 0


        current11 = passed_particles11/(steps-steady_state)
        current12 = passed_particles12/(steps-steady_state)
        current21 = passed_particles21/(steps-steady_state)
        current22 = passed_particles22/(steps-steady_state)
        current = current11+current12+current21+current22

        '''
        print('C_total:', current)
        print('C11:', current11)
        print('C12:', current12)
        print('C21', current21)
        print('C22', current22)
        '''
        C_total[m,n] = current
        C11[m,n] = current11
        C12[m,n] = current12
        C21[m,n] = current21
        C22[m,n] = current22

#init matrices
C_total = np.zeros([len(K12_1),len(K21_1)])  #total current
C11 = np.zeros([len(K12_1),len(K21_1)]) #current in l1 -> l1
C12 = np.zeros([len(K12_1),len(K21_1)]) #current in l1 -> l2
C21 = np.zeros([len(K12_1),len(K21_1)]) #current in l2 -> l1
C22 = np.zeros([len(K12_1),len(K21_1)]) #current in l2 -> l2

for m in range(len(K12_1)):
    print(m*'>',(len(K12_1)-m)*'-')

    for n in range(len(K21_1)):
        k12_1 = K12_1[m]      #setting the value of k12
        k21_1 = K21_1[n]      #setting the value of k21
        #initialize each outer loop
        L1, L2 = init_positions_particles1(N,int(M))
        #init
            #init the current measurement variables 'passed_particles'
        passed_particles11 = 0  #particles which passes 0th site latice 1 -> lattice 1
        passed_particles12 = 0  #particles which passed 0th site lattice 1 -> lattice 2
        passed_particles21 = 0  #particles which passed 0th site lattice 2 -> lattice 1
        passed_particles22 = 0  #particles which passed 0th site lattice 2 -> lattice 2
        current11 = 0
        current12 = 0
        current21 = 0
        current22 = 0
        current = 0


        for i in range(steps):
            for j in range(2*N+2):
                site = rd.randint(0,2*N+2)
                update(site)

            #cutoff (steady state) period
            if i == steady_state: #we start measuring from 0
                passed_particles11 = 0
                passed_particles12 = 0
                passed_particles21 = 0
                passed_particles22 = 0

        current11 = passed_particles11/(steps-steady_state)
        current12 = passed_particles12/(steps-steady_state)
        current21 = passed_particles21/(steps-steady_state)
        current22 = passed_particles22/(steps-steady_state)
        current = current11+current12+current21+current22

        C11[m,n] = current11
        C12[m,n] = current12
        C21[m,n] = current21
        C22[m,n] = current22
        C_total[m,n] = current

#saving the heatmaps into a txt file:
    #first rounding the matrices:
C11 = np.round(C11,3)
C12 = np.round(C12,3)
C21 = np.round(C21,3)
C22 = np.round(C22,3)
C_total = np.round(C_total,3)

Name = "PBC_heatmaps-N%s_s%s"%(N, steps)
heading = "sites: N%s, total steps: %s, steady_state: %s, rho_t: %rho_t\n ,k11_1 = %s, k12_1 = %s, k21_1 = %s, k22_1 =%s,"%(N, steps, steady_state, k11_1,K12_1, K21_1, k22_1)#" \t  \t "
rhos_t = str([round(i, 4) for i in rho_t])
rhos = str([round(i, 4) for i in density1])
gammas = str([round(i, 4) for i in density2])
heading = "Heatmaps of avg density, and avg current"
data = "\n","C11 matrix",C11,"\n","C12 matrix", C12,"\n","C21 matrix", C21,"\n","C22_matrix", C22,"\n", "C_total matrix", C_total
#data = np.array(data)
#data = np.transpose(data)
#fmt =  "%s", "%-10.4f","%s" ,"%-10.4f","%s","%-10.4f","%s", "%-10.4f","%s","%-10.4f"
np.savetxt(Name, data, fmt = '%-s', header = heading)

'''
#save the matrix into a txt
Name = "stuck_heatmapN%s_moreAverages"%(N)
heading = "parameters step: %s k12_values: %s \n k21_values %s \n"% (len(k12_values), k12_values, k21_values)
data = stuck_steps_matrix, "densities 1:", densities1,"densities2:",densities2
data = np.array(data)
#data = np.transpose(data)
#fmt = "%-10d", "%-10.3f", "%-10.3f"
np.savetxt(Name, data, fmt = "%-10d", delimiter = "\t", header = heading)
'''

'''
#plotting the density profiles
fig, (ax1, ax2) = plt.subplots(2)
fig.suptitle('Two-way lattice, sites=%s, steps:%s  \n parameters:  a1=%s, b1=%s, a2=%s, b2=%s, \n k11=%s, k12=%s, k22=%s, k21=%s'%(N, steps, a1, b1,a2,b2,k11,k12,k22,k21))
ax1.plot(range(1,N+1),densities1, linestyle = '-', marker = 'o', color = 'blue', label = 'Lattice 1')
#ax1.set_ylim([0.5,1])
ax1.set_xlim([0.65,N+0.9])
ax1.set_xlabel('site')
ax1.xaxis.set_major_locator(MaxNLocator(integer=True))
ax1.set_ylabel('average occupancy')
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
ax1.text(0.05, 0.95, "Current = %s"%round(current1,3), transform=ax1.transAxes, fontsize=9,
        verticalalignment='top', bbox=props)
for i in range(len(densities1)):
    ax1.text(i+1-0.2,densities1[i]+0.04,'ρ=%s'%round(densities1[i],3), verticalalignment='top',fontsize=9)
ax1.legend(loc = 1)
densities2 = np.flip(densities2)
ax2.plot(range(1,N+1),densities2, linestyle = '-', marker = 'o', color = 'red', label = 'Lattice 2') #to have the second lattice oriented the same way
#ax2.set_ylim([0,1])
ax2.set_xlim([0.5,N+0.9])
ax2.set_xlabel('site')
ax2.xaxis.set_major_locator(MaxNLocator(integer=True))
ax2.set_ylabel('average occupancy')
ax2.legend(loc = 1)     #loc 0  = best, loc 1 = right top
#ax2.text(0.05, 0.95, "Current = %s"%round(current2,3), transform=ax2.transAxes, fontsize=9,
#        verticalalignment='top', bbox=props)
for i in range(len(densities1)):
    ax2.text(i+1-0.2,densities2[i]+0.04,'γ=%s'%round(densities2[i],3), verticalalignment='top',fontsize=9)
t= now.strftime("%H:%M:%S")
plt.savefig('../../img/two-way/DensityProfile-N%sa1_%sb1_%s-a2_%sb2_%s-%s.png'%(N,a1,b1,a2,b2,t))
plt.show()
'''
