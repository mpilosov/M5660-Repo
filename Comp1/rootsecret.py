from secfun import secret_func
import numpy as np
myfun=secret_func()
left = -100. # set the right and left endpoints of our initial interval
right = 100.
x = left + (right - left)*np.random.rand() # pick an initial random guess in the interval
tol = 1E-9 # set desired tolerance
max_its = 5 # set desired max iterations before algorithm terminates
its_counter = 0 # initialize counter for iterations
err = tol*1E5 # initialize error as something larger than tolerance, it doesn't matter what.

while  (err > tol and its_counter < max_its) :  # set stopping criterion
    print '%d. x = %f'%(its_counter, x)
    x = x - myfun.eval(x)/myfun.deriv(x)
    its_counter += 1
print 'After %d iterations, we found our root to be %10f, '%(its_counter, x) + \
        'where the value of the secret function at this point is %10f'%(myfun.eval(x))
        
'''        
while  (err > tol and its_counter < max_its) :  # set stopping criterion
    print '[%f %f]'%(left, right)
    cen = left + 0.5*(right-left) # find midpoint. candidate for next interval upper/lower bound
    cen_val = myfun.eval(cen)
    left_val = myfun.eval(left)
    err = abs(cen_val)
    if cen_val*left_val>0: # if sign of function at midpoint matches on left
        left = cen # set the midpoint as new left-side of interval
    else: # otherwise
        right = cen # set the midpoint as the new right-side of the interval
    its_counter += 1
print 'After %d iterations, we found our root to be %10f, '%(its_counter, cen) + \
        'where the value of the secret function at this point is %10f'%(myfun.eval(cen))
'''