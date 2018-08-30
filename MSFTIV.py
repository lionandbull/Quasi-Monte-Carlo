import numpy as np
import scipy.optimize as optimization
from scipy.stats import norm

def func(K, sigma):
    r = 0.0111  ## 3 months risk-free rate, 10/26/17
    S0 = 78.76 ## The price of MSFT Stock at time: 4:00 pm, date: 10/26/2017
    T = 90.0/360
    d1 = (np.log(S0*1.0/K)+(r+0.5*sigma**2)*T)*1.0/(sigma*np.sqrt(T))
    d2 = d1-sigma*np.sqrt(T)
    C_model = S0*norm.cdf(d1)-K*np.exp(-r*T)*norm.cdf(d2)
    return C_model



Theta_list = []
Covariance = []
K = np.array([80, 85, 75, 82.5, 77.5, 70, 28, 72.5, 45, 60, 42, 65, 87.5,
              35, 62.5, 67.5, 30])
## Get the call option price from actual data
C_actual = [0.5 * (2.05+ 2.15), 0.5*(0.6+0.67), 0.5*(4.9+5.2), 0.5*(1.14+1.26),
            0.5 * (3.3 + 3.6), 0.5*(9.05+9.3), 0.5*(48.5+52.1), 0.5*(6.9+7.25),
            0.5*(33.6+34.25), 0.5*(18.75+19), 0.5*(36.45+37.65), 0.5 * (13.85 + 14.1),
            0.5*(0.26+0.35), 0.5*(43.8+43.9), 0.5*(16.3+16.55),0.5*(11.45+11.7),
            0.5 * (47.85 + 49.10)]

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



