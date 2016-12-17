from interpolant import *
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})
np.random.seed(40) # optional random seed for consistency

methods = ['Lagrange', 'Newton', 'Monomial']
# interpolation_method = methods[0] # if not using the for-loop
max_knots = 100



fun_choice = 'expoly' # choose a demonstration. 'cos' or 'randpoly' (random polynomial) or 'expoly' (for our example)
periods = 1 # FOR COS - specify number of periods in interval (make function more/less turbulent)
order = 3 # # FOR RANDPOLY - order of a randomly generated polynomial
root_min = 0. # FOR RANDPOLY - left endpoint of uniform random root distribution
root_max = 10. # FOR RANDPOLY - right endpoint of uniform random root distribution
roots = (b-a)*np.random.rand(order) + a # function is random polynomial (or rather, polynomial with randomly chosen roots)

a = 0 # left endpoint
b = 1 # right endpoint

view_plots = False
print_error = False
magnitude_error = 1E-16


# set high resolution discretization for plotting
hr_res_per_unit = 1000 # resolution for interval

plot_error_type_list = ['coeff', 'interpolant', 'original', 'perturbed'] # errors you wish to plot & save 

def mycos(x, freq, noise_opt = 0, magnitude_error = 1E-16):
    output = np.cos(2*np.pi*freq*x)#*np.exp(-1.0*x)
    # we use an additive noise model - uniform random centered at data with support 2*magnitude_error
    return output + noise_opt*(2*np.random.randn(len(x))-1)*magnitude_error

def rootpoly(x, roots, noise_opt = 0, magnitude_error = 1E-16):
    # generate random polynomial of a specified order, given by length of roots vector, with those roots
    output = np.ones(len(x))
    for i in range(len(roots)):
        output *= x - roots[i]
    temp_max = np.max(np.abs(output))
    output = output/temp_max
    # magnitude_error = magnitude_error*np.max(np.abs(output))
    return temp_max*( output + noise_opt*(2*np.random.randn(len(x))-1)*magnitude_error )# random perturbedurbations
    # return output + noise_opt*magnitude_error # uniform additive error
    
num_knots_range = range(3, 1+max_knots)
# num_knots = 5 # if not using for-loop: number of equispaced interpolating data points (one higher than desired order interpolating polynomial)
interpolant_error = np.zeros( (len(num_knots_range), 3) )
original_data_error = np.zeros( (len(num_knots_range), 3) ) # distance to true function
perturbed_data_error = np.zeros( (len(num_knots_range), 3) ) # distance to true function 
coefficient_error = np.zeros( (len(num_knots_range), 3) ) # max deviation in coefficients

for meth, interpolation_method in enumerate(methods):
    print('\n \t\t\t Working on %s Interpolation...'%interpolation_method)
    for row, num_knots in enumerate(num_knots_range):
        # b = num_knots - 2 # FOR VARIABLE INTERVAL LENGTH
        hr_res = (b-a)*hr_res_per_unit
        # hr_res = hr_res_per_unit
        x_data = np.linspace(a,b,num_knots) # create equispaced discretization
        x_hr = np.linspace(a,b,hr_res)

        if fun_choice == 'cos':
            # function is cos(periods*2*pi*x)
            y_data = mycos(x_data, periods, noise_opt = 0)
            y_data_perturbed = mycos(x_data, periods, noise_opt = 1, magnitude_error = magnitude_error)
            y_data_hr = mycos(x_hr, periods, noise_opt = 0)
        else:
            
            if fun_choice == 'expoly': # if we want our illustrative example of a deg 5 polynomial
                roots = [-0.9, -0.5, -0.3, 0.5, 0.8]
                # if you want to specify your own roots, do so HERE.
            y_data = rootpoly(x_data, roots, noise_opt = 0) # evaluate function at the control points for interpolation
            y_data_perturbed = rootpoly(x_data, roots, noise_opt = 1, magnitude_error = magnitude_error)
            y_data_hr = rootpoly(x_hr, roots, noise_opt = 0) # for plotting original function
            
        # Generate interpolants of pure and perturbedurbed data
        Q = Interpolant(x_data, y_data, interpolation_method)
        Qp = Interpolant(x_data, y_data_perturbed, interpolation_method)

        # Evaluate polynomial functions on a high resolution discretization for plotting
        y_interpolant = Q.eval(x_hr)
        y_perturbed_interpolant = Qp.eval(x_hr)

        # plot original function and control points
        plt.cla()
        plot1 = plt.plot(x_hr,y_data_hr, color='black')
        plot1 = plt.scatter(x_data, y_data, color = 'red')

        # plot interpolation polynomial generated from data points with and without purturbations
        plot1 = plt.plot(x_hr, y_interpolant, color = 'red', ls='-',lw =1)
        plot1 = plt.plot(x_hr, y_perturbed_interpolant, color = 'blue',ls = ':')
        
        # CHOOSE YOUR NORM 
        norm_choice = np.inf
        interpolant_error[row,meth] = np.linalg.norm(y_interpolant - y_perturbed_interpolant, norm_choice)
        original_data_error[row,meth] = np.linalg.norm(y_data_hr - y_interpolant, norm_choice)
        perturbed_data_error[row,meth] = np.linalg.norm(y_data_hr - y_perturbed_interpolant, norm_choice)
        coefficient_error[row,meth] = np.linalg.norm(Q.coeff - Qp.coeff, norm_choice)
        
        if view_plots:
            if num_knots > 65 and num_knots <68:
                plt.show() # show plot
    # plt.show() # show only final plot


fsize = 14 # specify font size for plots

# all but coeff are ERROR IN FUNCTION SPACE (approximation). 
# coeff error is error in finite-dim vector space of dim n+1
if fun_choice == 'cos':
    my_eq = '$f(x) = \cos(%d\pi x)$'%(2*periods)
else:
    my_eq = '$f(x) = '
    for xi in roots:
        if xi>=0:
            my_eq += '(x-%2.2f)'%xi
        else:
            my_eq += '(x+%2.2f)'%(-1.0*xi)
    my_eq+='$'

for error_type in plot_error_type_list: # Choose source of error to plot  
    if error_type == 'interpolant':   
        error = interpolant_error # coefficient_error | original_data_error | perturbed_data_error | interpolant_error
    elif error_type == 'original':
        error = original_data_error
    elif error_type == 'perturbed':
        error = perturbed_data_error 
    elif error_type == 'coeff':
        error = coefficient_error
    else:
        raise('ERROR: Specify one of "coeff", "interpolant", "original", "perturbed" in VAR plot_error_type_list')

    if print_error: # option to print error to terminal screen
        print ''
        print error
        print 'min:', num_knots_range[0],  'max:', num_knots_range[-1]

    # ACTUAL PLOTTING CODE
    plt.cla()
    plot2 = plt.plot(num_knots_range, error[:,0],'g') # Lagrange
    plot2 = plt.plot(num_knots_range, error[:,1],'b--') # Newton
    plot2 = plt.plot(num_knots_range, error[:,2],'k:') # Monomial
    
    plt.legend(methods,loc='upper left')
    plt.xlabel('Number of Equispaced Interpolating Points', size = fsize)
    plt.xlim([3,np.max(num_knots_range)])
    plt.yscale('log')
    
    if error_type == 'interpolant': # Choose source of error to plot    
        plt.ylim([1E-18, 1E3])
        plt.ylabel('Error (max norm) Between Interpolation\nwith and w/o Perturbed Data', size = fsize)
        plt.title('Sensitivity of Interpolating Methods to Perturbed Data\n\n %s'%my_eq, size = fsize+2)
        plt.savefig('TakeHomeFinal/%s_int_fun_error.eps'%my_eq)
        
    elif error_type == 'original':
        plt.ylim([1E-18, 1E3])
        plt.ylabel('Error (max norm) Between Unperturbed Interpolation\n and Target Function', size = fsize)
        plt.title('Interpolating Error as Function of # of Knots\n\n %s'%my_eq, size = fsize+2)
        plt.savefig('TakeHomeFinal/%s_unpert.eps'%my_eq)
        
    elif error_type == 'perturbed':
        plt.ylim([1E-18, 1E3])
        plt.ylabel('Error (max norm) Between Perturbed Interpolation\n and Target Function', size = fsize)
        plt.title('Interpolating Error (with Perturbed Data) as Function of # of Knots\n\n %s'%my_eq, size = fsize+2)
        plt.savefig('TakeHomeFinal/%s_pert.eps'%my_eq)
        
    elif error_type == 'coeff':
        plt.ylim([1E-24, 1E3])
        plt.ylabel('Error (max norm) Between Coefficients of Interpolation\nwith and w/o Perturbed Data', size = fsize)
        plt.title('Sensitivity of Interpolating Coefficients to Perturbed Data\n\n %s'%my_eq, size = fsize+2)
        plt.savefig('TakeHomeFinal/%s_error.eps'%my_eq)
    
    # plt.show() # show plot
    