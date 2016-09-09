def newton(x=0,tol=1E-8,iter=0):
    from math import fabs,pow,sqrt,log
    import cmath

    iter+=1
    #temp=x-(x**2-1)/(2*x)
    #temp=x-(x**4-1)/(4*x**3)
    temp=x-((x-1)**2*(x**2+1))/(2*(x-1)*(x**2+1)**2+(2*x+1)*(x-1)**2)
    #temp=x-(x**3-2*x+2)/(3*x**2-2)
    if iter >= 256:
        return [0,0,0,0]
    if abs(temp-x) < tol:
        r=x.real
        r=abs(r)/3.0
        g=abs(x.imag)/3.0
        b=(abs(x.real)-x.real+abs(x.imag)-x.imag)/6.0
        return [r,g,b,1.0/(.5*log(iter,2)+1)]
    else:
        return newton(temp,tol,iter)

import pylab as plt
import numpy as np

xdata=np.linspace(-2,2,400)
ydata=np.linspace(-2,2,300)
pixel=np.zeros([ydata.size,xdata.size,4])
xct=0
for x in xdata:
    yct=0
    for y in ydata:
        ans=newton(complex(x,y))
        pixel[yct,xct,:]=ans
        yct+=1
    xct+=1
plt.imshow(pixel)
#plt.xlabel(xdata)
#plt.ylabel(ydata)
plt.show()







