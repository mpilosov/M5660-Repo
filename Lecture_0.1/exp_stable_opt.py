import numpy as np
import pylab as plt

fsize = 14 						# font size for plots

def est_exp(x=1, order=5):   #give it a default order and input(returns e)
	'''
	computations of e^x that does not require an x0.  
	''' 						#TODO properly format function definition.
	
	c = np.log2(np.exp(1)) 		# the stored constant 'we have access to'
	oneoverc=1.0/c  #it's reciprocal, we will use it many times, multiply is faster than divide
	y = x*c 					# change of variables for cleanliness.
	dy = y - np.floor(y)  #good, always positive, even for negative x.
	result = np.ones_like(dy)
	temp=np.ones_like(dy) #we know that the first term is always one)
	for n in xrange(1,order+1): 	#xrange not range # compute terms in taylor series
		temp *= dy*oneoverc/float(n)
		#result += np.divide( np.divide(dy,c)**n, np.math.factorial(n) )  too many recomputes
		result += temp  #add term of taylor series to sum.
	return result*np.power(2, np.floor(y))
	
order = 5 						# choose the order of your taylor approximation
x_min = 0						# values of x you want to plot
x_max = 10
res = 400 						# linear spacing resolution
x = np.linspace(x_min, x_max, res) 
print 

est = est_exp(x, order) 		# the function can take vectors thanks to numpy
# generate plots
fig, ax = plt.subplots() 		# multiple plots all on figure 'ax'
ax.plot(x,np.abs(np.exp(x)-est)/np.exp(x))
plt.ylabel('\nRelative Error', fontsize=fsize)
plt.xlabel('\nValue of $x$',fontsize=fsize)
plt.show()						# show plot
# plt.savefig('good_approx_plot.png', dpi = 300) # save file

