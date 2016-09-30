"""
Numerical Analysis - MATH 5660 
Computational Assignment #2
@author: Michael Pilosov
"""

import numpy as np
import pylab as plt


initial_guess = -10          # choose an initial guess 
tol = 1E-14                     # set tolerance for root
err = 1                         # initialize error 

choose_root = np.random.rand()  # choose a random root
multiplicity = 2               # choose multiplicity of root at x = 0
mode = 'mod'

class fun:
    def __init__(self):
        self.root = choose_root
        self.calls = 0
        self.mult = multiplicity # (true multiplicity. )
        self.m = 2.0
        self.err = [1.0]
        
    def eval_f(self, x): # function evaluation x^m * (x - r)
        self.calls += 1
        return np.float128( (x**self.mult)*(x-self.root) )
        
    def eval_df(self, x): # function derivative
        self.calls += 1
        return np.float128( self.mult*( x**(self.mult - 1) )*(x-self.root) + x**self.mult )

    def iterate_Newton(self,x):
        return np.float128( x - fun.eval_f(x)/fun.eval_df(x) )
        
    def iterate_Modified_Newton(self,x):
        return np.float128( x - self.m*fun.eval_f(x)/fun.eval_df(x) )
        
    def iterate_hybrid_Newton(self,x):
        x = self.iterate_Modified_Newton(x)
        
        # if self.crit < 0.3 and old_crit < 0.3:
        # # if np.abs(self.change - old_change)/old_change< 0.3 and self.calls > 20:
        # # # if (np.abs((f - f_old)) < 2.5*np.abs(f)) and self.calls>40: # if relative change is small
        #     self.m+=1
        # #     self.calls = 0
        #     print 'Increasing assumed multiplicity.'
        #     return x
        # else: 
        return self.iterate_Modified_Newton(x)
        
fun = fun()
x = initial_guess
x_vec = []
lin_rate_vec = []
quad_rate_vec = []
print '%20s %20s '%('linear conv', 'quad conv')
while (err>tol):  # Newton's Method.
    if mode == 'hybrid':
        x = fun.iterate_hybrid_Newton(x)
    elif mode == 'mod':
        fun.m = multiplicity
        x = fun.iterate_Modified_Newton(x)
    elif mode == 'orig':
        x = fun.iterate_Newton(x)
    x_vec.append(x)
    f = fun.eval_f(x)
    err = np.abs(f) # our error - distance between function and 0 
    fun.err.append(err)
    rate_old = fun.err[-2]
    
    rate_f_quad = err/(rate_old**2)
    rate_f_lin = err/rate_old
    print '%20f %20f '%(rate_f_lin, rate_f_quad)
    
    lin_rate_vec.append(rate_f_lin)
    quad_rate_vec.append(rate_f_quad)
found_root = x
lin_rate_vec.pop(0)
quad_rate_vec.pop(0)
if found_root < 1E-7: # if we found the repeated root (0, not choose_root)
    choose_root = 0   # set true root to be 0 for proper comparisons.
    print('We found the repeated root!')
eval_root = fun.eval_f(found_root)
print('\nWe chose a random root in [0,1] (uniform distribution) \n \t and our initial guess was x = %f\n\n'%initial_guess )
print('The root we found was x = %2.15e.\n \t \tand f(x) = %2.15e'%(found_root, eval_root) )
print('The true root was %2.15e, \n \t \t which is within %2.15e of our estimate. \n'%(choose_root, np.abs(choose_root - found_root) ) )


fsize = 14
x_vec = np.array(x_vec)
fig, ax = plt.subplots() 		# multiple plots all on figure 'ax'
# plt.ylabel('Absolute Error', fontsize=fsize)

# ax.plot(range(len(lin_rate_vec)), lin_rate_vec, color='b' )
plt.ylabel('Convergence Rate', fontsize=fsize)
# ax.plot(range(len(quad_rate_vec)), quad_rate_vec, color='r')
plt.xlabel('Iterations', fontsize=fsize)
# plt.yscale('log')
# plt.xscale('log')
# plt.show()	




