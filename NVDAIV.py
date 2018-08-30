import numpy as np
import scipy.optimize as optimization
from scipy.stats import norm

def func(K, sigma):
    r = 0.0111  ## 3 months risk-free rate, 10/26/17
    S0 = 195.69  ## The price of NVDA Stock at close: 4:00 pm, date: 10/26/2017
    T = 90.0/360
    d1 = (np.log(S0*1.0/K)+(r+0.5*sigma**2)*T)*1.0/(sigma*np.sqrt(T))
    d2 = d1-sigma*np.sqrt(T)
    C_model = S0*norm.cdf(d1)-K*np.exp(-r*T)*norm.cdf(d2)
    return C_model



Theta_list = []
Covariance = []
K = np.array([200, 180, 195, 220, 170, 190, 210, 23, 165, 250, 260, 205, 90,
              160, 185, 270, 230, 290, 175])
## Get the call option price from actual data
C_actual = [0.5 * (12.9+13.2), 0.5*(23.85+24.25), 0.5*(15.25+15.6), 0.5*(6.4+6.55),
            0.5 * (30.65 + 31.4), 0.5*(17.9+18.1), 0.5*(9.2+9.45), 0.5*(171.5+176.1),
            0.5*(34.65+35.15), 0.5*(1.97+2.05), 0.5*(1.25+1.40), 0.5 * (10.95+ 11.25),
            0.5*(105.3 + 107.75), 0.5*(38.65+39.4), 0.5*(20.55+21.2),
            0.5 * (0.84 + 1), 0.5*(4.35+4.45), 0.5*(0.39+0.48), 0.5*(27.2+27.55)]

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



