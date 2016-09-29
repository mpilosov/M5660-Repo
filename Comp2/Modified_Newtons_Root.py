"""
Numerical Analysis - MATH 5660 
Computational Assignment #2
@author: Michael Pilosov
"""

import numpy as np
import pylab as plt


initial_guess = -20.             # choose an initial guess 
tol = 1E-16                     # set tolerance for root
err = 1                         # initialize error 
modify = True                   # Modified Newton's Method?

choose_root = np.random.rand()  # choose a random root
multiplicity = 2                # choose multiplicity of root at x = 0

class fun:
    def __init__(self):
        self.root = choose_root
        self.calls = 0
        self.mult = multiplicity
        
    def eval_f(self, x): # function evaluation x^m * (x - r)
        self.calls += 1
        return (x**self.mult)*(x-self.root)
        
    def eval_df(self, x): # function derivative
        self.calls += 1
        return self.mult*( x**(self.mult - 1) )*(x-self.root) + x**self.mult

    def iterate_Newton(self,x):
        return x - fun.eval_f(x)/fun.eval_df(x)
        
    def iterate_Modified_Newton(self,x):
        return x - self.mult*fun.eval_f(x)/fun.eval_df(x)
        
fun = fun()
x = initial_guess
x_vec = []
while (err>tol): 
    if not modify:
        x = fun.iterate_Newton(x) # Standard Newton's Method.
    else:
        x = fun.iterate_Modified_Newton(x) # Modified Newton's Method.
    x_vec.append(x)
    err = np.abs( fun.eval_f(x) )

found_root = x
if found_root < 1E-5: # if we found the repeated root (0, not choose_root)
    choose_root = 0   # set true root to be 0 for proper comparisons.
    print('We found the repeated root!')
eval_root = fun.eval_f(found_root)
print('We chose a random root in [0,1] (uniform distribution) \n \t and our initial guess was x = %f\n\n'%initial_guess )
print('The root we found was x = %2.15e.\n \t \tand f(x) = %2.15e'%(found_root, eval_root) )
print('The true (nonzero) root was %2.15e, \n \t \t which is within %2.15e of our estimate. \n'%(choose_root, np.abs(choose_root - found_root) ) )


fsize = 14
x_vec = np.array(x_vec)
fig, ax = plt.subplots() 		# multiple plots all on figure 'ax'
ax.plot( range(len(x_vec)), np.abs(x_vec - choose_root) )
plt.ylabel('Absolute Error', fontsize=fsize)
plt.xlabel('Iterations', fontsize=fsize)
# plt.yscale('log')
# plt.xscale('log')
plt.show()	




