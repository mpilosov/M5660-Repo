#import the libraries we'll need for this run
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stat
from mpl_toolkits.mplot3d import Axes3D


Samples=1000 # Number of Samples
alpha_samples=3.76E-5*stat.maxwell.rvs(size=Samples) #generate thermal diffusivity samples
heat_flux=np.zeros(Samples)  #initialize empty array of heat fluxes
beta_samples=stat.norm.rvs(0,.2,size=Samples) #generate flame centers

for loop in xrange(Samples):   #Sample (Outer Loop)
    alpha=alpha_samples[loop]  #PDE parameters for this sample(not neccesary, only for clarity)
    beta=beta_samples[loop]    
    gridsize=np.float(.05)    #spatial FD grid size
    timestep=1.0              #temporal time step
    steps=100                 #number of time steps
    points=np.int(1/.05)+1    #number of grid points
    x=np.linspace(0,1,num=points) #initialize numpy array of grid values
    U=np.zeros([points,steps+1])  #initialize numpy array of space X time temperature values
    A=-2*np.diagflat(np.ones(points-2))+np.diagflat(np.ones(points-3),-1)+np.diagflat(np.ones(points-3),1) #FD stencil
    f=np.float(100)/np.float(465)*np.exp(-50*(x-beta)**2)   #heat source
    B=np.diagflat(np.ones(points-2))-(timestep*alpha/gridsize**2)*A #Matrix for implicit Euler
    for timeloop in xrange(steps):
        data=timestep*f+U[:,timeloop]  #RHS for implicit Euler
        U[1:points-1,timeloop+1]=np.linalg.solve(B,data[1:points-1]) #Gaussian Elimination Solve

#Heat flux computation
    heat_flux[loop]=10*gridsize*alpha*(U[points-2,steps-1]-U[points-3,steps-1]/(2*gridsize)) #first interval
    heat_flux[loop]+=10*gridsize*alpha*(U[points-1,steps-1]-U[points-2,steps-1]/(2*gridsize)) #second interval 
#Solution Plotting, commented out
    #X,Y=np.meshgrid(np.linspace(0,100,num=steps+1),x)
    #fig = plt.figure()
    #ax = fig.add_subplot(111, projection='3d')
    #ax.plot_surface(X,Y,U,rstride=1,cstride=10)
    #plt.show()
    #end of sample loop
    #steady state solution for Current Sample
    #steady=np.linalg.solve(-alpha/gridsize**2*A,f[1:20])
#end sample loop
print heat_flux 
#plot histogram of heat fluxes
plt.hist(np.log10(-heat_flux), 50)
plt.xlabel('$\log_{10}$ heat flux')
plt.savefig('flux_hist.png', bbox_inches='tight')
