import numpy as np
import pylab as plt
import sys

#let us use Tex in our figure captions
plt.rc('text', usetex=True)


print 'epsilon=%g' % sys.float_info.epsilon
# output: 2.22045e-16
epsilon = sys.float_info.epsilon
print 'epsilon(hex) = %s' % float.hex(epsilon)
# output:  0x1.0000000000000p-52

y=np.linspace(1e-15,5e-17,3000) #vector of finite difference deltas
one = np.float64(1.0) 
two = np.float64(2.0)
x=np.divide((y+one)-one,y) #forward difference
x2=np.divide((one-one)+y,y) #rearranged forward difference
x3=np.divide((one+y)-(one-y),two*y) #central difference

fig, ax = plt.subplots() #multiple plots all on figure ax

plt.axvline(epsilon,color='r',linestyle='--') #plot vertical line for epsilon & annotate
ax.annotate(r"Machine $\varepsilon$",xy=(epsilon,1.5),xytext=(1.5*epsilon,1.75),arrowprops=dict(facecolor='black', shrink=0.05))

ax.plot(y,x, label='((x+1)-1)/x') # plot forward difference
ax.plot(y,x2,label='((1-1)+x)/x') # plot rearranged forward difference
ax.plot(y,x3, label='((1+x)-(1-x))/2x') # plot central difference
plt.ylim([-.1,2.1])
ax.legend() #print the legend in the default place("best")

#title 
plt.title(r"Difference Approximations to $f^\prime(x)=x, x=1$") # r is for not parsing special chars

plt.show()

#plt.savefig('cancel.png')  #optional save the figure

