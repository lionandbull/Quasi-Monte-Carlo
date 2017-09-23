import numpy as np
import scipy.optimize as optimization
from scipy.stats import norm

def func(K, sigma):
    r = 0.0222  ## 10 years risk-free rate, 08/14/17
    S0 = 161.66  ## The price of Apple Stock at time: 4:00 pm, date: 08/15/2017
    T = 66.0/360 ## data from 08/15 to 10/20
    d1 = (np.log(S0*1.0/K)+(r+0.5*sigma**2)*T)*1.0/(sigma*np.sqrt(T))
    d2 = d1-sigma*np.sqrt(T)
    C_model = S0*norm.cdf(d1)-K*np.exp(-r*T)*norm.cdf(d2)
    return C_model



Theta_list = []
Covariance = []
K = np.array([175, 165, 185, 160, 150, 170, 215, 140, 145, 210, 155, 180, 260, 90, 190, 70, 235, 225, 195, 245])
## Get the call option price from actual data
C_actual = [0.5 * (1.79+1.83), 0.5*(4.90+4.95), 0.5*(0.59+0.61), 0.5*(7.40+7.45),
            0.5 * (14.45 + 14.50), 0.5*(3.0+3.05), 0.5*(0.02+0.03),
            0.5 * (22.90 + 23.25), 0.5*(18.45+18.75), 0.5*(0.03+0.04), 0.5*(10.50+10.60),
            0.5 * (1.03 + 1.07), 0.5*(0+0.02), 0.5*(71.80+72.45), 0.5*(0.35+0.37),
            0.5 * (90.56 + 87.15), 0.5*(0+0.01), 0.5*(0.01+0.05), 0.5*(0.21+0.22), 0.5*(0.00+0.05)]

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



