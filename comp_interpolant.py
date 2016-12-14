from interpolant import *
import numpy as np
from matplotlib import pyplot as plt

np.random.seed(0)

methods = ['Lagrange', 'Newton', 'Monomial']
interpolation_method = methods[0]


fun_choice = 'cos' # choose a demonstration. 'cos' or 'poly'

def mycos(x, freq, noise_opt = 0, magnitude_error = 1E-16):
    output = np.cos(2*np.pi*freq*x)#*np.exp(-1.0*x)
    # we use an additive noise model - uniform random centered at data with support 2*magnitude_error
    return output + noise_opt*(2*np.random.randn(len(x))-1)*magnitude_error
    
def myfun(x, coeffs, noise_opt = 0, magnitude_error = 1E-16):
    # generate random polynomial of a specified order, given by length of coefficients vector
    order = len(coeffs)
    output = [coeffs[n]*np.power(x,n) for n in range(order)]
    output = sum(output,1)
    return output + noise_opt*(2*np.random.randn(len(x))-1)*magnitude_error

def randpoly(x, roots, noise_opt = 0, magnitude_error = 1E-16):
    # generate random polynomial of a specified order, given by length of coefficients vector
    output = np.ones(len(x))
    for i in range(len(roots)):
        output *= x - roots[i]
    output = output/np.max(np.abs(output))
    return output + noise_opt*(2*np.random.randn(len(x))-1)*magnitude_error # random perturbations
    # return output + noise_opt*magnitude_error # uniform additive error
    
magnitude_error = 1E-16
# if 1E-8, x^2 on [0,1] with 70 control points, we start seeing issues
# if 1E-4 with same situation, issues start around 20+ control points

order = 5 # order of a randomly generated polynomial
# coeffs = 2*np.random.rand(order+1)-1
# coeffs = [0,0,0,1] # x^3

a = 0. # left endpoint
b = 1. # right endpoint


# set high resolution discretization for plotting
hr_res = 500 
x_hr = np.linspace(a,b,hr_res)


# num_int_pts = 5 # number of equispaced interpolating data points (one higher than desired order interpolating polynomial)
num_int_pts_range = range(3,15)
error = np.zeros((len(num_int_pts_range), 3))
for meth, interpolation_method in enumerate(methods):
    print('\n \t\t\t %s INTERPOLATION\n'%interpolation_method)
    for row,num_int_pts in enumerate(num_int_pts_range):
        x_data = np.linspace(a,b,num_int_pts) # create equispaced discretization

        if fun_choice == 'cos':
            # function is cos(freq*2*pi*x)
            frequency = 1 # specify number of periods in interval (make function more/less turbulent)
            y_data = mycos(x_data, frequency, noise_opt = 0)
            y_data_pert = mycos(x_data, frequency, noise_opt = 1, magnitude_error = magnitude_error)
            y_hr = mycos(x_hr, frequency, noise_opt = 0)
        else:
            # function is random polynomial (or polynomial with chosen roots)
            # roots = (b-a)*np.random.rand(order+1) + a 
            roots = [-0.9, -0.5, -0.3, 0.5, 0.8]
            # roots = [0, 0]
            y_data = randpoly(x_data, roots, noise_opt = 0) # evaluate function at the control points for interpolation
            y_data_pert = randpoly(x_data, roots, noise_opt = 1, magnitude_error = magnitude_error)
            y_hr = randpoly(x_hr, roots, noise_opt = 0) # for plotting original function
            
        # Generate interpolants of pure and perturbed data
        Q = Interpolant(x_data, y_data, interpolation_method)
        Qp = Interpolant(x_data, y_data_pert, interpolation_method)

        # Evaluate polynomial functions on a high resolution discretization for plotting
        y_int_hr = Q.eval(x_hr)
        y_pert_int_hr = Qp.eval(x_hr)

        # plot original function and control points
        plt.cla()
        plot1 = plt.plot(x_hr,y_hr, color='black')
        plot1 = plt.scatter(x_data, y_data, color = 'red')

        # plot interpolation polynomial generated from data points with and without purturbations
        plot1 = plt.plot(x_hr, y_int_hr, color = 'red', ls='-',lw =2)
        plot1 = plt.plot(x_hr, y_pert_int_hr, color = 'red',ls = '--')
        
        inf_norm = np.linalg.norm(y_int_hr - y_pert_int_hr, np.inf)
        # print 'I = %2d, Max diff b/n interpolating polynomials is %2.4e, 2-norm is %2.4e'%(num_int_pts, inf_norm, np.linalg.norm(y_int_hr - y_pert_int_hr)) 
        error[row,meth] = inf_norm
        # show plot 
        # plt.show()
    # plt.show()
# print np.insert( error, 0, num_int_pts_range, axis=1)
print error
print num_int_pts_range
plt.cla()
plot2 = plt.plot(num_int_pts_range,error[:,0],'g') # Lagrange
plot2 = plt.plot(num_int_pts_range,error[:,1],'b') # Newton
plot2 = plt.plot(num_int_pts_range,error[:,2],'k--') # Monomial
plt.legend(methods,'upper left')
plt.xlabel('Number of Equispaced Interpolating Points')
plt.ylabel('Error (max norm) between Interpolation\nwith and w/o Perturbed Data')
plt.title('Sensitivity of Interpolating Methods to Perturbed Data')
plt.xlim([3,np.max(num_int_pts_range)])
plt.show()