import numpy as np
import scipy.optimize as optimization
from scipy.stats import norm

def func(K, sigma):
    r = 0.0111  ## 3 months risk-free rate, 08/15/17
    S0 = 153.06  ## The price of IBM Stock at time: 4:04 pm, date: 10/26/2017
    T = 90.0/360
    d1 = (np.log(S0*1.0/K)+(r+0.5*sigma**2)*T)*1.0/(sigma*np.sqrt(T))
    d2 = d1-sigma*np.sqrt(T)
    C_model = S0*norm.cdf(d1)-K*np.exp(-r*T)*norm.cdf(d2)
    return C_model



Theta_list = []
Covariance = []
K = np.array([155, 160, 180, 165, 65, 150, 195, 230, 80, 170, 215, 140, 60, 175, 115])
## Get the call option price from actual data
C_actual = [0.5 * (3.9+4.1), 0.5*(2.1+2.28), 0.5*(0.18+0.19), 0.5*(1.05+1.14),
            0.5 * (95 + 99.35), 0.5*(6.55+6.75), 0.5*(0.03+0.08), 0.5*(0+0.06),
            0.5*(80.4+84.5), 0.5*(0.52+0.58), 0.5*(0+0.13), 0.5*(14.15+14.55), 0.5*(100.05+104.45),
            0.5 * (0.28 + 0.31), 0.5*(45.1+49.45)]

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



