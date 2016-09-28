from secfun import secret_func
# import numpy as np
myfun=secret_func()
left = -100. # set the right and left endpoints of our initial interval
right = 100.
# x = left + (right - left)*np.random.rand() # pick an initial random guess in the interval
tol = 1E-12 # set desired tolerance
bisect_max_its = 12 # set desired max iterations before bisection algorithm terminates
newton_max_its = 0.5*(24-bisect_max_its-1) # use desired max iterations before newton's algorithm terminates
its_counter = 0 # initialize counter for iterations
err = tol*1E5 # initialize error as something larger than tolerance, it doesn't matter what.

# First we bisect. Each reduces the search interval by a factor of 2.
# 8 iterations leads to an interval of length < 1
print 'Bisection Method \n'
left_val = myfun.eval(left)
while  (err > tol and its_counter < bisect_max_its) :  # set stopping criterion
    print '%d. [%f %f]'%(its_counter, left, right)
    cen = left + 0.5*(right-left) # find midpoint. candidate for next interval upper/lower bound
    cen_val = myfun.eval(cen)
    err = abs(cen_val)
    if cen_val*left_val>0: # if sign of function at midpoint matches on left
        left = cen # set the midpoint as new left-side of interval
    else: # otherwise
        right = cen # set the midpoint as the new right-side of the interval
    its_counter += 1
print 'After %d iterations, we reduced our interval to be [%f %f]'%(bisect_max_its, left, right)
print 'We now switch to Newton''s Method for the remainder of our iterations.'

# Then we use Newton's Method to refine our estimate
x = left + (right - left)*0.5 # use midpoint of interval as starting guess.
its_counter = 0
while  (err > tol and its_counter < newton_max_its) :  # set stopping criterion
    print '%d. x = %f'%(its_counter, x)
    eval_x = myfun.eval(x)
    err = abs(eval_x)
    x = x - eval_x/myfun.deriv(x) # Newton's iterate - fixed point method
    its_counter += 1

# print x, myfun.deriv(x)
# print myfun.deriv(x)
print 'After %d iterations, we found our root to be %1.16f, '%(its_counter, x) + \
        'where the value of the secret function at this point is %e'%(eval_x)
print 'If this isn''t enough accuracy, we can increment bisect_max_its by 1 and try again.'