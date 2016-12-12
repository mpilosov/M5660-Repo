from interpolant import *
import numpy as np
from matplotlib import pyplot as plt

interpolation_method = 'Lagrange'


def myfun(x, freq, noise_opt = 0):
    return np.cos(2*np.pi*freq*x) + noise_opt*np.random.randn(len(x))*1E-16

frequency = 1 # specify number of periods in interval (make function more/less turbulent)
noise_option = 1 # perturb outputs?

a = 0 # left endpoint
b = 1 # right endpoint
num_pts = 4 # number of data points (one higher than desired order interpolating polynomial)
x_data = np.linspace(a,b,num_pts) # create equispaced discretization


hr_res = 100 # set high resolution discretization for plotting
x_hr = np.linspace(a,b,hr_res)
y_hr = myfun(x_hr, frequency, noise_opt = 0) # for plotting original function
# evaluate function at the control points for interpolation
y_data = myfun(x_data, frequency, noise_opt = 0)
y_data_pert = myfun(x_data, frequency, noise_opt = 1)


Q = Interpolant(x_data, y_data, interpolation_method)
Qp = Interpolant(x_data, y_data_pert, interpolation_method)

y_int_hr = Q.eval(x_hr)
y_pert_int_hr = Qp.eval(x_hr)

# plot original function and control points
plot1 = plt.plot(x_hr,y_hr, color='blue')
plot1 = plt.scatter(x_data, y_data, color = 'red')

# plot interpolation polynomial with and without purturbation
plot1 = plt.plot(x_hr, y_int_hr, color = 'red')
plot1 = plt.plot(x_hr, y_pert_int_hr, color = 'yellow')

# show plot 
plt.show()
