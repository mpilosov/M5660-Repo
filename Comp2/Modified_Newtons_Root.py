"""
Numerical Analysis - MATH 5660 
Computational Assignment #2
@author: Michael Pilosov
"""

import numpy as np
import pylab as plt


initial_guess = 40.0            # choose an initial guess 
tol = 1E-64                      # set tolerance for root
err = 1                          # initialize error 


mode = 'orig'                    # Choose mode. orig / mod / hybrid

choose_root = 10                 # choose a random root
multiplicity = 2                # choose multiplicity of root at x = 0

class fun:
    def __init__(self, choose_root=np.random.rand(), multiplicity=2):
        self.root = choose_root
        self.calls = 0
        self.mult = multiplicity
        self.m = 1
        self.x_vals = []
        self.present_x = None
        self.rate = None
        self.old_rate = None
        
    def eval_f(self, x): # function evaluation x^m * (x - r)
        return np.float128( (x**self.mult)*(x-self.root) )
        
    def eval_df(self, x): # function derivative
        return np.float128( self.mult*( x**(self.mult - 1) )*(x-self.root) + x**self.mult )


    def iterate_Newton(self,x):
        self.present_x = np.float128( x - fun.eval_f(x)/fun.eval_df(x) )
        self.x_vals.append(self.present_x)
        return self.present_x
        
    def iterate_Modified_Newton(self,x):
        self.present_x = np.float128( x - self.m*fun.eval_f(x)/fun.eval_df(x) )
        self.x_vals.append(self.present_x)
        return self.present_x
        
        
    def iterate_hybrid_Newton(self,x):
        self.calls += 1
        if self.rate is not None and self.old_rate is not None and self.calls>5:
            # print self.rate/self.old_rate 
            if self.rate/self.old_rate > 0.99:
                self.m = np.floor(1.0/(1.0 - self.rate))
                print 'Changing m to %d'%(self.m)
                self.calls = 0 # reset counter to make sure we give modified newton's a chance first.
        self.present_x = self.iterate_Modified_Newton(x)
        return self.present_x
        
fun = fun(choose_root=choose_root, multiplicity=multiplicity)
x = initial_guess
x_vec = []
first_flag = 0
x_ratio = []
x_ratio2 = []
print( '\n-----------------------------------------------' )
print('Our initial guess was x = %f\n'%initial_guess )
print( '\t %20s %20s'%('linear rate', 'quadratic rate') )
while (err>tol): 
    if mode == 'hybrid':                    # hybrid newton - should be quadratic conv for both types of root (depending on inital guess) 
        
        x = fun.iterate_hybrid_Newton(x)

    elif mode == 'mod':                     # modified newton - quad conv for repeated root, no conv for simple.
        fun.m = multiplicity                # set correct multiplicity (assume known)
        x = fun.iterate_Modified_Newton(x)
        
    elif mode == 'orig':                    # standard newton - lin conv for repeated root, quad for simple.
        x = fun.iterate_Newton(x)
        
    
    x_vec.append(x)
    
    if first_flag < 2: # compute conv rate approximations on the fly.
        first_flag += 1
    else:
        x_1 = fun.x_vals[-2]
        x_2 = fun.x_vals[-3]
        x_ratio.append( np.abs( (x - x_1)/(x_1 - x_2) ) )        # linear convergence rate
        x_ratio2.append( np.abs( (x - x_1)/((x_1 - x_2)**2) ) )  # quadratic convergence rate
        
        fun.rate = x_ratio[-1]
        if len(x_ratio)>1:
            fun.old_rate = x_ratio[-2]
        print '\t %20e %20e'%(x_ratio[-1], x_ratio2[-1])
    
    
    err = np.abs( fun.eval_f(x) )

# m = 1 /( 1 - rate_observed)

found_root = x
if found_root != choose_root: # if we found the repeated root (0, not choose_root)
    choose_root = 0   # set true root to be 0 for proper comparisons.
    print('----We found the repeated root!----')
eval_root = fun.eval_f(found_root)

print('We found x = %f.\n \t \tand f(x) = %2.15e'%(found_root, eval_root) )
print('The true root was %2.15e, \n \t \t which is within %2.15e of our estimate. \n'%(choose_root, np.abs(choose_root - found_root) ) )


fsize = 14

x_vec = np.array(x_vec)
fig, ax = plt.subplots() 		# multiple plots all on figure 'ax'
temp=np.abs(x_vec-choose_root)
ratio=temp[1:]/temp[0:-1]
ratio2=temp[1:]/temp[0:-1]**2


# print x_ratio
# print ratio
# print ' '
# print x_ratio2
# print ratio2


ax.plot( range(len(x_ratio)), x_ratio )
if mode != 'mod':
    ax.plot( range(len(ratio)-1), x_ratio2 ) # don't look at quadratic for regular newton's on repeated root.

#ax.plot( range(len(x_vec)), np.abs(x_vec - choose_root) )
plt.ylabel('Convergence Rate', fontsize=fsize)
plt.xlabel('Iterations', fontsize=fsize)
# plt.yscale('log')
# plt.xscale('log')
plt.show()	





