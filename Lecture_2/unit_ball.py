import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def mat_norm(A=np.array([[1.0, .5],[-.3,2.0]]),p=2,plot=True):
    xvec=2*np.random.rand(2,1000)-1 #generate 1000 random points in [-1,-1]x[1,1]
    #normalize them so they have p-norm length 1.
    xnrm=np.linalg.norm(xvec,ord=p,axis=0) 
    xvec=xvec/xnrm #normalize each vector, hopefully
    b=A.dot(xvec)
    Anrm=np.max(np.linalg.norm(b,ord=p,axis=0))
    if plot: #olot x-ball, A-ball
        plt.subplot(121)
        plt.scatter(xvec[0],xvec[1],s=.2)
        ttl='Unit ball in '+str(p)+'-norm'
        plt.title(ttl)
        plt.subplot(122)
        plt.scatter(b[0],b[1],color='red',s=.2)
        ax=plt.gca()
        ttl=str(p)+'-'+'norm of A='+str(Anrm)
        plt.title(ttl)
        ax.set_aspect('equal')
        plt.show()
    return Anrm

def norm_perturb(A=np.array([[4,-1],[2,2]]),b=np.array([3,4]),eps=1E-6,samples=10000):
    x0=np.linalg.solve(A,b)
    plt.scatter(x0[0],x0[1],s=1,color='red')
    condA=np.linalg.cond(A,np.inf)
    normA=np.linalg.norm(A,np.inf)
    normb=np.linalg.norm(b,np.inf)    
    X=np.zeros([2,samples])
    for loop in xrange(samples):
        deltaA=normA*eps*(2*np.random.rand(2,2)-1)
        deltab=normb*eps*(2*np.random.rand(2)-1)
        X[:,loop]=np.linalg.solve(A+deltaA,b+deltab)
    plt.scatter(X[0],X[1],s=.2)
    plt.xlim([x0[0]-2*condA*eps,x0[0]+2*condA*eps])
    plt.ylim([x0[1]-2*condA*eps,x0[1]+2*condA*eps])
    ax=plt.gca()
    ax.set_aspect('equal')
    ax.add_patch(patches.Rectangle((x0[0]-eps,x0[1]-eps),2.0*eps,2.0*eps,fill=False,color='red'))
    plt.show()
    



        
    

