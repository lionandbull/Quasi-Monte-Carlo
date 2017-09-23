import numpy as np
import scipy.optimize as optimization
from scipy.stats import norm

def func(K, sigma):
    r = 0.0222  ## 10 years risk-free rate, 08/14/17
    S0 = 73.22 ## The price of MSFT Stock at time: 4:00 pm, date: 08/15/2017
    T = 66.0/360 ## data from 08/15 to 10/20
    d1 = (np.log(S0*1.0/K)+(r+0.5*sigma**2)*T)*1.0/(sigma*np.sqrt(T))
    d2 = d1-sigma*np.sqrt(T)
    C_model = S0*norm.cdf(d1)-K*np.exp(-r*T)*norm.cdf(d2)
    return C_model



Theta_list = []
Covariance = []
K = np.array([75, 72.5, 80, 85, 77.5, 62.5, 37.5, 70, 60, 65, 57.5, 45, 67.5,
              47.5, 55])
## Get the call option price from actual data
C_actual = [0.5 * (1.4+1.43), 0.5*(2.66+2.7), 0.5*(0.22+0.27), 0.5*(0.03+0.05),
            0.5 * (0.6 + 0.65), 0.5*(11.05+11.2), 0.5*(33.9+34.6), 0.5*(4.35+4.45),
            0.5*(13.5+13.6), 0.5*(8.7+8.85), 0.5*(15.90+16.05), 0.5 * (28.30 + 28.65),
            0.5*(6.45+6.55), 0.5*(25.85+25.95), 0.5*(18.40+18.55)]

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



