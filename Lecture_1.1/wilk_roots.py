import numpy as np
from sympy import Symbol
from sympy.polys.polytools import   poly_from_expr
import matplotlib.pyplot as plt

x = Symbol('x')
W = 1
for i in range(1, 21):
    W = W * (x-i)

P,d = poly_from_expr(W.expand())
p = P.all_coeffs()
print p
x = np.arange(1, 21)
plt.scatter(x,np.zeros(20),c=x)

for l in xrange(0,100):
    ptilde=p*(1+1E-11*np.random.rand(21))

    roots=np.roots(ptilde)

    X = roots.real 
    Y = roots.imag 
    plt.scatter(X,Y, c=x, s=.5)

roots=np.roots(p)
print roots

plt.grid()    
plt.show()

