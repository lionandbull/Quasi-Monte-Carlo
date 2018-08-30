import numpy as np
import scipy.optimize as optimization
from scipy.stats import norm

def func(K, sigma):
    r = 0.0111  ## 3 months risk-free rate, 08/15/17
    S0 = 157.41  ## The price of Apple Stock at close: 4:00 pm, date: 10/26/2017
    T = 90.0/360
    d1 = (np.log(S0*1.0/K)+(r+0.5*sigma**2)*T)*1.0/(sigma*np.sqrt(T))
    d2 = d1-sigma*np.sqrt(T)
    C_model = S0*norm.cdf(d1)-K*np.exp(-r*T)*norm.cdf(d2)
    return C_model



Theta_list = []
Covariance = []
K = np.array([165, 160, 170, 175, 155, 150, 140, 225, 255, 190, 210, 205, 185, 215, 180, 145, 220, 240, 295, 195])
## Get the call option price from actual data
C_actual = [0.5 * (3.9+4), 0.5*(5.8+5.9), 0.5*(2.52+2.60), 0.5*(1.62+1.66),
            0.5 * (8.25 + 8.40), 0.5*(11.3+11.45), 0.5*(18.85+19.15),
            0.5 * (0.02 + 0.07), 0.5*(0+0.06), 0.5*(0.39+0.42), 0.5*(0.08+0.1),
            0.5 * (0.11 + 0.14), 0.5*(0.62+0.66), 0.5*(0.06+0.09), 0.5*(1.02+1.04),
            0.5 * (14.8 + 15.05), 0.5*(0.03+0.06), 0.5*(0+0.04), 0.5*(0+0.03), 0.5*(0.25+0.27)]

## Get Theta_list
#sigma_list = np.array([0.2, 0.3, 0.02, 3])
sigma_list = np.array([0.4, 0.04, 0.1, 0.2])
data_error = []
for i in range(0,len(C_actual)):
    data_error.append(1)
data_error = np.asarray(data_error)

for i in range(0,len(sigma_list)):
    Theta_list.append(optimization.curve_fit(func,  K, C_actual,  sigma_list[i], data_error)[0])
    #Covariance.append(optimization.curve_fit(func, K, C_actual, sigma_list[i], data_error)[1])
print("The parameter estimate is: " + str(Theta_list))
#print("The covariance is: " + str(Covariance))



