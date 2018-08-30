import numpy as np
import scipy.optimize as optimization
from scipy.stats import norm

def func(K, sigma):
    r = 0.0111  ## 3 months risk-free rate, 10/26/17
    S0 = 12.27  ## The price of F Stock at time: 4:00 pm, date: 10/26/2017
    T = 90.0/360
    d1 = (np.log(S0*1.0/K)+(r+0.5*sigma**2)*T)*1.0/(sigma*np.sqrt(T))
    d2 = d1-sigma*np.sqrt(T)
    C_model = S0*norm.cdf(d1)-K*np.exp(-r*T)*norm.cdf(d2)
    return C_model



Theta_list = []
Covariance = []
K = np.array([12, 13, 15, 14.75, 11.75, 9.75, 21.75, 6, 19.75, 10, 16.75, 17, 24.75, 4.75])
## Get the call option price from actual data
C_actual = [0.5 * (0.62+0.65), 0.5*(0.19+0.21), 0.5*(0+0), 0.5*(0.02+0.03),
            0.5 * (0.79 + 0.82), 0.5*(2.55+2.65), 0.5*(0+0.02), 0.5*(5.9+6.35), 0.5*(0+0.03),
            0.5 * (0 + 0), 0.5*(0+0.01), 0.5*(0+0.02), 0.5*(0+0.02), 0.5*(7.2+7.9)]

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



