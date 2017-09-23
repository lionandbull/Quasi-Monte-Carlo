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


for i in range(3, 6):
    times = 0
    for j in np.arange(10 ** (i - 1), 10 ** i, (10 ** i - 10 ** (i - 1)) / 100):
        j = int(j)
        times += 1
        MC_price.setIteration(j)
        QMC_price.setIteration(j)
        Xaxis.append(j)
        MC.append(MC_price.pricingByMC())
        QMC.append(QMC_price.pricingByQMC())
        print("Running times: " + str(times))



plt.plot(Xaxis, MC, "r--", label = "Monte Carlo")
plt.plot(Xaxis, QMC, label = "Halton Quasi-Monte Carlo")
plt.xlabel("Number of simulations")
plt.ylim(np.mean(QMC) - 1, np.mean(QMC) + 1)
plt.ylabel("Price")
plt.xscale('log')

plt.legend()
plt.show()




