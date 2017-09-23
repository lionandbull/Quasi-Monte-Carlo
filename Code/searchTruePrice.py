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

MC_price = PricingBO_MC(100, 50, 0.0219, 0.15, 0.01, 1000, corr, [0.35, 0.3, 0.1, 0.1, 0.15], 0.227, 0.381,
                                0.159, 0.202, 0.171)
QMC_price = PricingBO_QMC(100, 50, 0.0219, 0.15, 0.01, 1000, corr, [0.35, 0.3, 0.1, 0.1, 0.15], 0.227, 0.381,
                                0.159, 0.202, 0.171)

QMC_price.generatePrimeInt()
QMC_price.generateHaltonSequences()
Xaxis = []
MC = []
QMC = []
for i in range(15):
    MC_price.setIteration(20000 + i * 1000)
    QMC_price.setIteration(20000 + i * 1000)

    MC.append(MC_price.pricingByMC())
    QMC.append(QMC_price.pricingByQMC())
    Xaxis.append(20000 + i * 1000)
    print("times: " + str(i))

plt.plot(Xaxis, MC, "r--", label = "Monte Carlo")
plt.plot(Xaxis, QMC, label = "Halton Quasi-Monte Carlo")
plt.xlabel("Number of iterations")
plt.ylabel("Price")
plt.ylim((np.mean(MC) + np.mean(QMC)) / 2 - 0.5, (np.mean(MC) + np.mean(QMC)) / 2 + 0.5)
plt.legend()
plt.show()
print(MC)
print(QMC)