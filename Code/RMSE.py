from Correlation import Correlation
from BasketOption_QMC import PricingBO_QMC
from BasketOption_MC import PricingBO_MC
import matplotlib.pyplot as plt
import numpy as np
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

Xaxis = []
MC = []
QMC = []
MC_price = PricingBO_MC(100, 50, 0.0219, 0.15, 0.01, 1000, corr, [0.35, 0.3, 0.1, 0.1, 0.15], 0.227, 0.381,
                                0.159, 0.202, 0.171)
QMC_price = PricingBO_QMC(100, 50, 0.0219, 0.15, 0.01, 1000, corr, [0.35, 0.3, 0.1, 0.1, 0.15], 0.227, 0.381,
                                0.159, 0.202, 0.171)
QMC_price.generatePrimeInt()
QMC_price.generateHaltonSequences()

## True prices
MC_price.setIteration(20000)
true_price_MC = MC_price.pricingByMC()
QMC_price.setIteration(20000)
true_price_QMC = QMC_price.pricingByQMC()
print("finished")
## RMSE

def RMSE_QMC(m, n):
    difference = []
    QMC_price.setIteration(n)
    for i in range(m):
        difference.append( (QMC_price.pricingByQMC() - true_price_QMC) ** 2 )
        print(str(i))
    return np.sqrt(sum(difference) / m)


def RMSE_MC(m, n):
    difference = []
    MC_price.setIteration(n)
    for i in range(m):
        difference.append( (MC_price.pricingByMC() - true_price_MC) ** 2 )
        print(str(i))
    return np.sqrt(sum(difference) / m)

for i in range(4):
    QMC.append( RMSE_QMC(50, 10 ** (1 + i)) )
    MC.append( RMSE_MC(50, 10 ** (1 + i)) )
    Xaxis.append(10 ** (1 + i))
    print("Times: " + str(i))

plt.plot(Xaxis, MC, "r--", label = "Monte Carlo")
plt.plot(Xaxis, QMC, label = "Halton Quasi-Monte Carlo")
plt.legend()
plt.ylim(10 ** (-4), 10 ** 0)
plt.xscale('log')
plt.yscale('log')

plt.ylabel("RMSE")
plt.xlabel("Number of iterations")
plt.show()
