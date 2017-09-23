import numpy as np
import scipy.optimize as optimization
from scipy.stats import norm

def func(K, sigma):
    r = 0.0222  ## 10 years risk-free rate, 08/14/17
    S0 = 166.98  ## The price of NVDA Stock at time: 4:00 pm, date: 08/15/2017
    T = 66.0/360 ## data from 08/15 to 10/20
    d1 = (np.log(S0*1.0/K)+(r+0.5*sigma**2)*T)*1.0/(sigma*np.sqrt(T))
    d2 = d1-sigma*np.sqrt(T)
    C_model = S0*norm.cdf(d1)-K*np.exp(-r*T)*norm.cdf(d2)
    return C_model



Theta_list = []
Covariance = []
K = np.array([165, 170, 180, 175, 200, 210, 160, 120, 125, 155, 150, 185, 230,
              240, 195, 270, 190, 145, 250, 220])
## Get the call option price from actual data
C_actual = [0.5 * (11.9+12.15), 0.5*(9.55+9.75), 0.5*(6+6.15), 0.5*(7.55+7.8),
            0.5 * (2.19 + 2.30), 0.5*(1.32+1.36), 0.5*(14.55+14.90), 0.5*(47.05+48.95),
            0.5*(42.25+43.95), 0.5*(17.75+18.20), 0.5*(21.10+21.80), 0.5 * (4.65 + 5),
            0.5*(0.5+0.53), 0.5*(0.31+0.33), 0.5*(2.84+2.94),
            0.5 * (0.07 + 0.15), 0.5*(3.65+3.85), 0.5*(24.95+25.80), 0.5*(0.21+0.22), 0.5*(0.79+0.83)]

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



