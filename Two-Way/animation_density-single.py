#animate lattice
import visualiser as vis
import numpy as np
import scipy
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy.random as rd
import random as random
from os import path




#parameters
N = 30     # number of sites
a1 = 0.2      # injection probability at lattice 1
a2 = 0     # injection probability at lattice 2
b1 = 0.2     # removal probability at lattice 1
b2 = 1      # removal probability at lattice 2
k11 = 1     # steping probability for particle 1 in lattice 1
k12 = 0    # steping probability for particle 1 to lattice 2
k21 = 0     # steping probability for particle 2 to lattice 1
k22 = 1     # steping probability for particle 2 in lattice 2

steps = 100*N*N+422000#50000*N#000*N                 #steps
steady_state = 100*N*N+400000#35000*N# 25*N          #after the transient phase we start the animation
precomputation = steps-steady_state-1000#20*N*N#steps-steady_state-1000  #when it only records the density prof but does not visualise


#animation
frames = 2  #how many transition images we have
j = 0       #init counter
d_low = 0.0 #density plot bounds
d_high = 0.9 #density plot bounds

#init
L1 = np.zeros(N)    #initialize lattice 1
L2 = np.zeros(N)    #initialize lattice 2
densities1 = np.zeros(N) #average occupation density for each site in lattice 1
densities2 = np.zeros(N) #average occupation density for each site in lattice 2
densities1_sum = np.zeros(N) #in order to get momental densities we create the entire historical sum
densities2_sum = np.zeros(N) #in order to get momental densities we create the entire historical sum
passed_particles1 = 0  #particles which passes 0th site in latice 1
passed_particles2 = 0  #particles which passed 0th site in latice 2
current1 = 0
current2 = 0
#update ftion
def update(i):
    global passed_particles1
    #insertion a1
    if i==0:
        if L1[0]==0 and rd.rand()<a1:
            L1[0]=1
            passed_particles1 +=1###
    #in case there site = 1 there is particle 2 which should leave
    elif i==1 and L1[0]==2 and rd.rand()<b2: #in case there is particle 2 it leaves
        L1[0]=0

    #insertion a2
    elif i==N+1:
        if L2[0]==0 and rd.rand()<a2:
            L2[0]=2
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

            #continue in the opposite lane
            elif L1[i-1]==0 and rd.rand()<k21:
                L1[i]=0
                L1[i-1]=2

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

            #continue in the opposite lane
            elif L2[i-1]==0 and rd.rand()<k12:
                if not i==0:
                    L2[i]=0
                    L2[i-1]=1

def update_anim(i,ax1,ax2):
    global j,passed_particles1, current1


    #insertion a1
    if i==0:
        if L1[0]==0 and rd.rand()<a1:
            passed_particles1 +=1
            for k in range(frames):
                '''
                fig, ax = plt.subplots()
                ax.set_aspect(aspect=1)
                vis.lattice_grid(N,2,ax)

                positions1_1, positions1_2, positions2_2, positions2_1 = vis.lattice2positions(L1, L2,ax)
                '''
                L1[0]=1


                positions1_1, positions1_2, positions2_2, positions2_1,fig,ax1,ax2 = plot_init()

                vis.lattice_points(positions1_2, 0, "r", ax1)
                vis.lattice_points(N-1-positions2_2, 1, "r", ax1)#to flip it N-1-positions_vect
                vis.lattice_points(N-1-positions2_1, 1, "b", ax1)
                positions1_1[0] = positions1_1[0]-1+(k+1)/frames
                vis.lattice_points(positions1_1, 0, "b", ax1)


                #density plotting
                fig.suptitle('TASEP open lattice visualisation and corresponding density profile, sites=%s  \n parameters:  a1=%s, b1=%s'%(N, a1, b1))
                ax2.plot(range(1,N+1),densities1, linestyle = '-', color = 'blue', label = 'Lattice 1')
                #ax2.plot(range(1,N+1),np.flip(densities2), linestyle = '-', color = 'red', label = 'Lattice 2')
                ax2.set_ylim([d_low,d_high])
                #ax2.set_ylim([0,1.0])
                #ax2.set_xlim([0,N])
                ax2.set_xlabel('site')
                ax2.set_ylabel('average occupancy')
                props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
                #ax2.text(0.05, 0.95, "Current = %s"%round(current1,3), transform=ax2.transAxes, fontsize=9,
                        #verticalalignment='top', bbox=props)
                ax2.legend(loc = 1)



                outpath = '../../img/visualiser/'
                plt.savefig(path.join(outpath,"%s-.png"%(j)))
                j+=1

            plt.close('all')

    #in case there site = 1 there is particle 2 which should leave
    elif i==1 and L1[0]==2 and rd.rand()<b2: #in case there is particle 2 it leaves
        for k in range(frames):
            positions1_1, positions1_2, positions2_2, positions2_1,fig,ax1,ax2 = plot_init()

            vis.lattice_points(positions1_1, 0, "b", ax1)
            vis.lattice_points(N-1-positions2_2, 1, "r", ax1)
            vis.lattice_points(N-1-positions2_1, 1, "b", ax1)
            positions1_2[-1] = positions1_2[-1]-(k+1)/frames
            vis.lattice_points(positions1_2, 0, "r", ax1)

            #density plotting
            fig.suptitle('TASEP open lattice visualisation and corresponding density profile, sites=%s  \n parameters:  a1=%s, b1=%s'%(N, a1, b1))
            ax2.plot(range(1,N+1),densities1, linestyle = '-', color = 'blue', label = 'Lattice 1')
            #ax2.plot(range(1,N+1),np.flip(densities2), linestyle = '-', color = 'red', label = 'Lattice 2')
            ax2.set_ylim([d_low,d_high])#ax2.set_ylim([0,1.0])
            #ax2.set_xlim([0,N])
            ax2.set_xlabel('site')
            ax2.set_ylabel('average occupancy')
            props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
            #ax2.text(0.05, 0.95, "Current = %s"%round(current1,3), transform=ax2.transAxes, fontsize=9,
                    #verticalalignment='top', bbox=props)
            ax2.legend(loc = 1)


            outpath = '../../img/visualiser/'
            plt.savefig(path.join(outpath,"%s-.png"%(j)))
            j+=1
        L1[0]=0
        plt.close('all')

    #insertion a2
    elif i==N+1:
        if L2[0]==0 and rd.rand()<a2:
            L2[0]=2
            for k in range(frames):
                positions1_1, positions1_2, positions2_2, positions2_1,fig,ax1,ax2 = plot_init()

                vis.lattice_points(positions1_1, 0, "b", ax1)
                vis.lattice_points(positions1_2, 0, "r", ax1)
                vis.lattice_points(N-1-positions2_1, 1, "b", ax1)
                positions2_2[0] = positions2_2[0]-1+(k+1)/frames
                vis.lattice_points(N-1-positions2_2, 1, "r", ax1)


                fig.suptitle('TASEP open lattice visualisation and corresponding density profile, sites=%s  \n parameters:  a1=%s, b1=%s'%(N, a1, b1))
                ax2.plot(range(1,N+1),densities1, linestyle = '-', color = 'blue', label = 'Lattice 1')
                #ax2.plot(range(1,N+1),np.flip(densities2), linestyle = '-', color = 'red', label = 'Lattice 2')
                ax2.set_ylim([d_low,d_high])#ax2.set_ylim([0,1.0])
                #ax2.set_xlim([0,N])
                ax2.set_xlabel('site')
                ax2.set_ylabel('average occupancy')
                props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
                #ax2.text(0.05, 0.95, "Current = %s"%round(current1,3), transform=ax2.transAxes, fontsize=9,
                        #verticalalignment='top', bbox=props)
                ax2.legend(loc = 1)


                outpath = '../../img/visualiser/'
                plt.savefig(path.join(outpath,"%s-.png"%(j)))
                j+=1

            plt.close('all')
    #in case site = 2N+1 and there is particle 1 it leaves
    elif i==N+2 and L2[0]==1 and rd.rand()<b2: #in case there is particle 1 it leaves

        for k in range(frames):
            positions1_1, positions1_2, positions2_2, positions2_1,fig,ax1,ax2= plot_init()

            vis.lattice_points(positions1_1, 0, "b", ax1)
            vis.lattice_points(positions1_2, 0, "r", ax1)
            vis.lattice_points(N-1-positions2_2, 1, "r", ax1)
            positions2_1[0] = positions2_1[0]-(k+1)/frames
            vis.lattice_points(N-1-positions2_1, 1, "b", ax1)

            fig.suptitle('TASEP open lattice visualisation and corresponding density profile, sites=%s  \n parameters:  a1=%s, b1=%s'%(N, a1, b1))
            ax2.plot(range(1,N+1),densities1, linestyle = '-', color = 'blue', label = 'Lattice 1')
            #ax2.plot(range(1,N+1),np.flip(densities2), linestyle = '-', color = 'red', label = 'Lattice 2')
            ax2.set_ylim([d_low,d_high])#ax2.set_ylim([0,1.0])
            #ax2.set_xlim([0,N])
            ax2.set_xlabel('site')
            ax2.set_ylabel('average occupancy')
            props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
            #ax2.text(0.05, 0.95, "Current = %s"%round(current1,3), transform=ax2.transAxes, fontsize=9,
                    #verticalalignment='top', bbox=props)
            ax2.legend(loc = 1)


            outpath = '../../img/visualiser/'
            plt.savefig(path.join(outpath,"%s-.png"%(j)))
            j+=1
        L2[0]=0
        plt.close('all')
    #removal b1
    elif i==N and rd.rand()<b1:
        if L1[-1]>0:

            for k in range(frames):
                positions1_1, positions1_2, positions2_2, positions2_1,fig,ax1,ax2= plot_init()

                vis.lattice_points(N-1-positions2_2, 1, "r", ax1)
                vis.lattice_points(positions1_2, 0, "r", ax1)
                vis.lattice_points(N-1-positions2_1, 1, "b", ax1)
                if np.size(positions1_1)>0:
                    positions1_1[-1] = positions1_1[-1]+(k+1)/frames
                vis.lattice_points(positions1_1, 0, "b", ax1)

                fig.suptitle('TASEP open lattice visualisation and corresponding density profile, sites=%s  \n parameters:  a1=%s, b1=%s'%(N, a1, b1))
                ax2.plot(range(1,N+1),densities1, linestyle = '-', color = 'blue', label = 'Lattice 1')
                #ax2.plot(range(1,N+1),np.flip(densities2), linestyle = '-', color = 'red', label = 'Lattice 2')
                ax2.set_ylim([d_low,d_high])#ax2.set_ylim([0,1.0])
                #ax2.set_xlim([0,N])
                ax2.set_xlabel('site')
                ax2.set_ylabel('average occupancy')
                props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
                #ax2.text(0.05, 0.95, "Current = %s"%round(current1,3), transform=ax2.transAxes, fontsize=9,
                        #verticalalignment='top', bbox=props)
                ax2.legend(loc = 1)


                outpath = '../../img/visualiser/'
                plt.savefig(path.join(outpath,"%s-.png"%(j)))
                j+=1
            L1[-1]=0
            plt.close('all')
    #removal b2
    elif i==2*N+1 and rd.rand()<b2:
        if L2[-1]>0:
            for k in range(frames):
                positions1_1, positions1_2, positions2_2, positions2_1,fig,ax1,ax2= plot_init()

                vis.lattice_points(positions1_1, 0, "b", ax1)
                vis.lattice_points(positions1_2, 0, "r", ax1)
                vis.lattice_points(N-1-positions2_1, 1, "b", ax1)
                if np.size(positions2_2)>0:
                    positions2_2[-1] = positions2_2[-1]+(k+1)/frames
                vis.lattice_points(N-1-positions2_2, 1, "r", ax1)

                fig.suptitle('TASEP open lattice visualisation and corresponding density profile, sites=%s  \n parameters:  a1=%s, b1=%s'%(N, a1, b1))
                ax2.plot(range(1,N+1),densities1, linestyle = '-', color = 'blue', label = 'Lattice 1')
                #ax2.plot(range(1,N+1),np.flip(densities2), linestyle = '-', color = 'red', label = 'Lattice 2')
                ax2.set_ylim([d_low,d_high])#ax2.set_ylim([0,1.0])
                #ax2.set_xlim([0,N])
                ax2.set_xlabel('site')
                ax2.set_ylabel('average occupancy')
                props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
                #ax2.text(0.05, 0.95, "Current = %s"%round(current1,3), transform=ax2.transAxes, fontsize=9,
                        #verticalalignment='top', bbox=props)
                ax2.legend(loc = 1)


                outpath = '../../img/visualiser/'
                plt.savefig(path.join(outpath,"%s-.png"%(j)))
                j+=1
            L2[-1]=0
            plt.close('all')
    #regular site lattice 1
    elif i>0 and i < N:
        i = i-1
        #update particle 1
        if L1[i]==1:
            #make a step
            if L1[i+1]==0 and rd.rand()<k11:
                for k in range(frames):
                    positions1_1, positions1_2, positions2_2, positions2_1,fig,ax1,ax2= plot_init()

                    vis.lattice_points(N-1-positions2_2, 1, "r", ax1)
                    vis.lattice_points(positions1_2, 0, "r", ax1)
                    vis.lattice_points(N-1-positions2_1, 1, "b", ax1)
                    if np.size(positions1_1)>0:
                        ind = np.where(positions1_1==i)
                        positions1_1[ind] = positions1_1[ind]+(k+1)/frames
                    vis.lattice_points(positions1_1, 0, "b", ax1)

                    fig.suptitle('TASEP open lattice visualisation and corresponding density profile, sites=%s  \n parameters:  a1=%s, b1=%s'%(N, a1, b1))
                    ax2.plot(range(1,N+1),densities1, linestyle = '-', color = 'blue', label = 'Lattice 1')
                    #ax2.plot(range(1,N+1),np.flip(densities2), linestyle = '-', color = 'red', label = 'Lattice 2')
                    ax2.set_ylim([d_low,d_high])#ax2.set_ylim([0,1.0])
                    #ax2.set_xlim([0,N])
                    ax2.set_xlabel('site')
                    ax2.set_ylabel('average occupancy')
                    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
                    #ax2.text(0.05, 0.95, "Current = %s"%round(current1,3), transform=ax2.transAxes, fontsize=9,
                            #verticalalignment='top', bbox=props)
                    ax2.legend(loc = 1)


                    outpath = '../../img/visualiser/'
                    plt.savefig(path.join(outpath,"%s-.png"%(j)))
                    j+=1
                L1[i]=0
                L1[i+1]=1
                plt.close('all')


            #overtake
            elif L1[i+1]>0 and L2[-i-2]==0 and rd.rand()<k12:
                for k in range(frames):
                    positions1_1, positions1_2, positions2_2, positions2_1,fig,ax1,ax2= plot_init()

                    vis.lattice_points(N-1-positions2_2, 1, "r", ax1)
                    vis.lattice_points(positions1_2, 0, "r", ax1)
                    vis.lattice_points(N-1-positions2_1, 1, "b", ax1)
                    if np.size(positions1_1)>0:
                        ind = np.where(positions1_1==i)
                        positions1_1[ind] = positions1_1[ind]+(k+1)/frames
                        vis.lattice_points(positions1_1[ind], (k+1)/frames, "b", ax1)
                    vis.lattice_points(np.delete(positions1_1, ind), 0, "b", ax1)

                    fig.suptitle('TASEP open lattice visualisation and corresponding density profile, sites=%s  \n parameters:  a1=%s, b1=%s'%(N, a1, b1))
                    ax2.plot(range(1,N+1),densities1, linestyle = '-', color = 'blue', label = 'Lattice 1')
                    #ax2.plot(range(1,N+1),np.flip(densities2), linestyle = '-', color = 'red', label = 'Lattice 2')
                    ax2.set_ylim([d_low,d_high])#ax2.set_ylim([0,1.0])
                    #ax2.set_xlim([0,N])
                    ax2.set_xlabel('site')
                    ax2.set_ylabel('average occupancy')
                    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
                    #ax2.text(0.05, 0.95, "Current = %s"%round(current1,3), transform=ax2.transAxes, fontsize=9,
                            #verticalalignment='top', bbox=props)
                    ax2.legend(loc = 1)


                    outpath = '../../img/visualiser/'
                    plt.savefig(path.join(outpath,"%s-.png"%(j)))
                    j+=1
                L1[i]=0
                L2[-i-2]=1
                plt.close('all')

        #update particle 2
        if L1[i]==2:

            #finish overtaking
            if L2[-i]==0 and rd.rand()<k21:

                for k in range(frames):
                    positions1_1, positions1_2, positions2_2, positions2_1,fig,ax1,ax2= plot_init()

                    vis.lattice_points(N-1-positions2_2, 1, "r", ax1)
                    vis.lattice_points(positions1_1, 0, "b", ax1)
                    vis.lattice_points(N-1-positions2_1, 1, "b", ax1)
                    if np.size(positions1_2)>0:
                        ind = np.where(positions1_2==i)
                        positions1_2[ind] = positions1_2[ind]-(k+1)/frames
                        vis.lattice_points(positions1_2[ind], (k+1)/frames, "r", ax1)
                    vis.lattice_points(np.delete(positions1_2, ind), 0, "r", ax1)

                    fig.suptitle('TASEP open lattice visualisation and corresponding density profile, sites=%s  \n parameters:  a1=%s, b1=%s'%(N, a1, b1))
                    ax2.plot(range(1,N+1),densities1, linestyle = '-', color = 'blue', label = 'Lattice 1')
                    #ax2.plot(range(1,N+1),np.flip(densities2), linestyle = '-', color = 'red', label = 'Lattice 2')
                    ax2.set_ylim([d_low,d_high])#ax2.set_ylim([0,1.0])
                    #ax2.set_xlim([0,N])
                    ax2.set_xlabel('site')
                    ax2.set_ylabel('average occupancy')
                    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
                    #ax2.text(0.05, 0.95, "Current = %s"%round(current1,3), transform=ax2.transAxes, fontsize=9,
                            #verticalalignment='top', bbox=props)
                    ax2.legend(loc = 1)


                    outpath = '../../img/visualiser/'
                    plt.savefig(path.join(outpath,"%s-.png"%(j)))
                    j+=1

                L1[i]=0
                L2[-i]=2
                plt.close('all')
            #continue in the opposite lane
            elif L1[i-1]==0 and rd.rand()<k21:
                for k in range(frames):
                    positions1_1, positions1_2, positions2_2, positions2_1,fig,ax1,ax2= plot_init()

                    vis.lattice_points(N-1-positions2_2, 1, "r", ax1)
                    vis.lattice_points(positions1_2, 0, "r", ax1)
                    vis.lattice_points(N-1-positions2_1, 1, "b", ax1)
                    if np.size(positions1_1)>0:
                        ind = np.where(positions1_1==i)
                        positions1_1[ind] = positions1_1[ind]+(k+1)/frames
                    vis.lattice_points(positions1_2, 0, "b", ax1)

                    fig.suptitle('TASEP open lattice visualisation and corresponding density profile, sites=%s  \n parameters:  a1=%s, b1=%s'%(N, a1, b1))
                    ax2.plot(range(1,N+1),densities1, linestyle = '-', color = 'blue', label = 'Lattice 1')
                    #ax2.plot(range(1,N+1),np.flip(densities2), linestyle = '-', color = 'red', label = 'Lattice 2')
                    ax2.set_ylim([d_low,d_high])#ax2.set_ylim([0,1.0])
                    #ax2.set_xlim([0,N])
                    ax2.set_xlabel('site')
                    ax2.set_ylabel('average occupancy')
                    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
                    #ax2.text(0.05, 0.95, "Current = %s"%round(current1,3), transform=ax2.transAxes, fontsize=9,
                            #verticalalignment='top', bbox=props)
                    ax2.legend(loc = 1)


                    outpath = '../../img/visualiser/'
                    plt.savefig(path.join(outpath,"%s-.png"%(j)))
                    j+=1
                L1[i]=0
                L1[i-1]=2
                plt.close('all')
    #regular site lattice 2
    elif i>N and i<2*N+1:
        i = i-N-2
        #print(i)
        assert(i>=0)
        assert(i<=N)

        #update particle 2
        if L2[i]==2:
            #make a step
            if L2[i+1]==0 and rd.rand()<k22:
                for k in range(frames):
                    positions1_1, positions1_2, positions2_2, positions2_1,fig,ax1,ax2= plot_init()

                    vis.lattice_points(positions1_1, 0, "b", ax1)
                    vis.lattice_points(positions1_2, 0, "r", ax1)
                    vis.lattice_points(N-1-positions2_1, 1, "b", ax1)
                    if np.size(positions2_2)>0:
                        ind = np.where(positions2_2==i)
                        positions2_2[ind] = positions2_2[ind]+(k+1)/frames
                    vis.lattice_points(N-1-positions2_2, 1, "r", ax1)

                    fig.suptitle('TASEP open lattice visualisation and corresponding density profile, sites=%s  \n parameters:  a1=%s, b1=%s'%(N, a1, b1))
                    ax2.plot(range(1,N+1),densities1, linestyle = '-', color = 'blue', label = 'Lattice 1')
                    #ax2.plot(range(1,N+1),np.flip(densities2), linestyle = '-', color = 'red', label = 'Lattice 2')
                    ax2.set_ylim([d_low,d_high])#ax2.set_ylim([0,1.0])
                    #ax2.set_xlim([0,N])
                    ax2.set_xlabel('site')
                    ax2.set_ylabel('average occupancy')
                    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
                    #ax2.text(0.05, 0.95, "Current = %s"%round(current1,3), transform=ax2.transAxes, fontsize=9,
                            #verticalalignment='top', bbox=props)
                    ax2.legend(loc = 1)


                    outpath = '../../img/visualiser/'
                    plt.savefig(path.join(outpath,"%s-.png"%(j)))
                    j+=1
                L2[i]=0
                L2[i+1]=2
                plt.close('all')
            #overtake
            elif L2[i+1]>0 and L1[-i-2]==0 and rd.rand()<k21:
                for k in range(frames):
                    positions1_1, positions1_2, positions2_2, positions2_1,fig,ax1,ax2= plot_init()

                    vis.lattice_points(positions1_1, 0, "b", ax1)
                    vis.lattice_points(positions1_2, 0, "r", ax1)
                    vis.lattice_points(N-1-positions2_1, 1, "b", ax1)
                    if np.size(positions2_2)>0:
                        ind = np.where(positions2_2==i)
                        positions2_2[ind] = positions2_2[ind]+(k+1)/frames
                        vis.lattice_points(N-1-positions2_2[ind], 1-(k+1)/frames, "r", ax1)
                    vis.lattice_points(N-1-np.delete(positions2_2, ind), 1, "r", ax1)

                    fig.suptitle('TASEP open lattice visualisation and corresponding density profile, sites=%s  \n parameters:  a1=%s, b1=%s'%(N, a1, b1))
                    ax2.plot(range(1,N+1),densities1, linestyle = '-', color = 'blue', label = 'Lattice 1')
                    #ax2.plot(range(1,N+1),np.flip(densities2), linestyle = '-', color = 'red', label = 'Lattice 2')
                    ax2.set_ylim([d_low,d_high])#ax2.set_ylim([0,1.0])
                    #ax2.set_xlim([0,N])
                    ax2.set_xlabel('site')
                    ax2.set_ylabel('average occupancy')
                    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
                    #ax2.text(0.05, 0.95, "Current = %s"%round(current1,3), transform=ax2.transAxes, fontsize=9,
                            #verticalalignment='top', bbox=props)
                    ax2.legend(loc = 1)


                    outpath = '../../img/visualiser/'
                    plt.savefig(path.join(outpath,"%s-.png"%(j)))
                    j+=1
                L2[i]=0
                L1[-i-2]=2
                plt.close('all')
        #update particle 1
        if L2[i]==1:
            #finish overtaking
            if L1[-i]==0 and rd.rand()<k12:
                for k in range(frames):
                    positions1_1, positions1_2, positions2_2, positions2_1,fig,ax1,ax2= plot_init()

                    vis.lattice_points(N-1-positions2_2, 1, "r", ax1)
                    vis.lattice_points(positions1_1, 0, "b", ax1)
                    vis.lattice_points(positions1_2, 0, "r", ax1)
                    if np.size(positions2_1)>0:
                        ind = np.where(positions2_1==i)
                        positions2_1[ind] = positions2_1[ind]-(k+1)/frames
                        vis.lattice_points(N-1-positions2_1[ind], 1-(k+1)/frames, "b", ax1)
                    vis.lattice_points(N-1-np.delete(positions2_1, ind), 1, "b", ax1)

                    fig.suptitle('TASEP open lattice visualisation and corresponding density profile, sites=%s  \n parameters:  a1=%s, b1=%s'%(N, a1, b1))
                    ax2.plot(range(1,N+1),densities1, linestyle = '-', color = 'blue', label = 'Lattice 1')
                    #ax2.plot(range(1,N+1),np.flip(densities2), linestyle = '-', color = 'red', label = 'Lattice 2')
                    ax2.set_ylim([d_low,d_high])#ax2.set_ylim([0,1.0])
                    #ax2.set_xlim([0,N])
                    ax2.set_xlabel('site')
                    ax2.set_ylabel('average occupancy')
                    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
                    #ax2.text(0.05, 0.95, "Current = %s"%round(current1,3), transform=ax2.transAxes, fontsize=9,
                            #verticalalignment='top', bbox=props)
                    ax2.legend(loc = 1)


                    outpath = '../../img/visualiser/'
                    plt.savefig(path.join(outpath,"%s-.png"%(j)))
                    j+=1
                L2[i]=0
                L1[-i]=1
                plt.close('all')

            #continue in the opposite lane
            elif L2[i-1]==0 and rd.rand()<k12:
                if not i==0:
                    for k in range(frames):
                        positions1_1, positions1_2, positions2_2, positions2_1,fig,ax1,ax2= plot_init()

                        vis.lattice_points(N-1-positions2_2, 1, "r", ax1)
                        vis.lattice_points(positions1_1, 0, "b", ax1)
                        vis.lattice_points(positions1_2, 0, "r", ax1)
                        if np.size(positions2_1)>0:
                            ind = np.where(positions2_1==i)
                            positions2_1[ind] = positions2_1[ind]-(k+1)/frames
                            vis.lattice_points(N-1-positions2_1[ind], 1, "b", ax1)
                        vis.lattice_points(np.delete(N-1-positions2_1, ind), 1, "b", ax1)

                        fig.suptitle('TASEP open lattice visualisation and corresponding density profile, sites=%s  \n parameters:  a1=%s, b1=%s'%(N, a1, b1))
                        ax2.plot(range(1,N+1),densities1, linestyle = '-', color = 'blue', label = 'Lattice 1')
                        ##ax2.plot(range(1,N+1),np.flip(densities2), linestyle = '-', color = 'red', label = 'Lattice 2')
                        ax2.set_ylim([d_low,d_high])#ax2.set_ylim([0,1.0])
                        #ax2.set_xlim([0,N])
                        ax2.set_xlabel('site')
                        ax2.set_ylabel('average occupancy')
                        props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
                        #ax2.text(0.05, 0.95, "Current = %s"%round(current1,3), transform=ax2.transAxes, fontsize=9,
                                #verticalalignment='top', bbox=props)
                        ax2.legend(loc = 1)


                        outpath = '../../img/visualiser/'
                        plt.savefig(path.join(outpath,"%s-.png"%(j)))
                        j+=1
                    L2[i]=0
                    L2[i-1]=1
                    plt.close('all')
def plot_init():

    fig, (ax1, ax2) = plt.subplots(2)
    ax1.set_aspect(aspect=1)
    vis.lattice_grid(N,1,ax1)###
    positions1_1, positions1_2, positions2_2, positions2_1= vis.lattice2positions(L1, L2,ax1)
    return positions1_1, positions1_2, positions2_2, positions2_1,fig, ax1, ax2



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
        #print('reg1')###

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
                #print('balba')###
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
step = 0
while step<steady_state: #just simulate and dont produce plots before the steady_state
    print("pre: ",step) ###
    site = rd.randint(0,2*N+2)
    update(site)
    #DisplayNice()
    step+=1

while step>=steady_state and step<steady_state+precomputation:
    print(step)###
    site = rd.randint(0,2*N+2)
    update(site)
    #DisplayNice()

    #measure density
    l1 = L1>0           #remove ones and twos -> boolean
    l1 = l1.astype(int) #make them integers
    l2 = L2>0           #remove ones and twos -> boolean
    l2 = l2.astype(int) #make them integers

    for k in range(N):
        densities1_sum[k] += l1[k]    #add to the density
        densities2_sum[k] += l2[k]    #add to the density
        densities1[k] = densities1_sum[k]/(step-steady_state)
        densities2[k] = densities2_sum[k]/(step-steady_state)

    step+=1

    if step == steady_state:
        passed_particles1 = 0

while j<(steps-steady_state-precomputation) and step>=steady_state+precomputation:
    print("j: ", j)

    fig, (ax1, ax2) = plt.subplots(2)
    ax1.set_aspect(aspect=1)
    #vis.lattice_grid(N,1,ax)#vis.lattice_grid(N,2,ax)

    #site = int(input("ch: "))#rd.randint(0,2*N+2)
    site = rd.randint(0,2*N+2)
    #print(site)
    update_anim(site,ax1, ax2)






    positions1_1, positions1_2, positions2_2, positions2_1 = vis.lattice2positions(L1, L2,ax1)
    vis.lattice_points(positions1_1, 0, "b", ax1)
    vis.lattice_points(positions1_2, 0, "r", ax1)
    vis.lattice_points(N-1-positions2_2, 1, "r", ax1)#to flip it N-1-positions_vect
    vis.lattice_points(N-1-positions2_1, 1, "b", ax1)
    plt.close('all')

    #update site densities
    step+=1
    if step>=steady_state:
        print(passed_particles1)
        current1 = passed_particles1/(step-steady_state) #update the current
        l1 = L1>0           #remove ones and twos -> boolean
        l1 = l1.astype(int) #make them integers
        l2 = L2>0           #remove ones and twos -> boolean
        l2 = l2.astype(int) #make them integers

        for k in range(N):
            densities1_sum[k] += l1[k]    #add to the density
            #densities2_sum[k] += l2[k]    #add to the density
            densities1[k] = densities1_sum[k]/(step-steady_state)
            #densities2[k] = densities2_sum[k]/(step-steady_state)





'''
    positions1_1, positions1_2, positions2_2, positions2_1 = vis.lattice2positions(L1, L2,ax)
    vis.lattice_points(positions1_1, 0, "b", ax)
    vis.lattice_points(positions1_2, 0, "r", ax)
    vis.lattice_points(N-1-positions2_2, 1, "r", ax)#to flip it N-1-positions_vect
    vis.lattice_points(N-1-positions2_1, 1, "b", ax)

    outpath = '../../img/visualiser/'
    #plt.savefig(path.join(outpath,"%s-.png"%(j)))
'''
    #j+=1


#plt.show()
