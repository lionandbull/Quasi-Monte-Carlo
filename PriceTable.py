from Correlation import Correlation
from BasketOption_QMC import PricingBO_QMC
from BasketOption_MC import PricingBO_MC
from prettytable import PrettyTable
import numpy as np
import matplotlib.pyplot as plt


## Generate corr matrix

corrMatrix = Correlation('AAPL.csv', 'IBM.csv', 'NVDA.csv', 'MSFT.csv', 'F.csv')
corrMatrix.getPriceList()
corrMatrix.setWeight(0.94)
corrMatrix.calReturns()
corrMatrix.calReturnsSquare()
corrMatrix.calVolatility()
corrMatrix.calCovariance()
corrMatrix.calCorr()
corr = corrMatrix.corr

## Prcing option and making table

def auxiliaryFucQMC(K):
    a = PricingBO_QMC([157.41, 153.06, 195.69, 78.76, 12.27], K, 0.0111, 0.25, 0.01, 20000, corr, [0.35, 0.3, 0.1, 0.1, 0.15], 0.219, 0.383, 0.155, 0.173,
                                0.166)
    a.generatePrimeInt()
    a.generateHaltonSequences()
    return a.pricingByQMC()

def auxiliaryFucMC(K):
    a = PricingBO_MC([157.41, 153.06, 195.69, 78.76, 12.27], K, 0.0111, 0.25, 0.01, 20000, corr, [0.35, 0.3, 0.1, 0.1, 0.15], 0.219, 0.383, 0.155, 0.173,
                                0.166)
    return a.pricingByMC()

Xaxis = []
Yaxis_QMC = []
Yaxis_MC = []
QMC = ["Quasi-Monte-Carlo"]
MC = ["Monte-Carlo"]
for i in np.arange(100, 140, 5):
    Xaxis.append(i)
    Yaxis_QMC.append(auxiliaryFucQMC(i))
    QMC.append(auxiliaryFucQMC(i))
    Yaxis_MC.append(auxiliaryFucMC(i))
    MC.append(auxiliaryFucMC(i))

x = PrettyTable(["Value", "K = 100", "K = 105", "K = 110", "K = 115", "K = 120", "K = 125", "K = 130", "K = 135"])
x.align["Value"] = "l"
x.padding_width = 1
x.add_row(QMC)
x.add_row(MC)

print(x)

## Plot

plt.plot(Xaxis, Yaxis_QMC, color = 'red', label = "QMC method")
plt.plot(Xaxis, Yaxis_MC, color = "blue", label = "MC method")
plt.legend()
plt.ylabel("Prices")
plt.xlabel("strike prices")
plt.show()

