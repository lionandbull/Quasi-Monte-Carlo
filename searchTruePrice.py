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

# for i in range(1,100):
#     MC_price = PricingBO_MC([157.41, 153.06, 195.69, 78.76, 12.27], 100, 0.0111, 0.25, 0.01, 1000, corr,
#                             [0.35, 0.3, 0.1, 0.1, 0.15], 0.219, 0.383, 0.155, 0.173,
#                             0.166)
#     QMC_price = PricingBO_QMC([157.41, 153.06, 195.69, 78.76, 12.27], 100, 0.0111, 0.25, 0.01, 1000, corr,
#                               [0.35, 0.3, 0.1, 0.1, 0.15], 0.219, 0.383, 0.155, 0.173,
#                               0.166)
#     QMC_price.generatePrimeInt()
#     QMC_price.generateHaltonSequences()
#     MC_price.setIteration(i*100)
#     QMC_price.setIteration(i*100)
#
#     MC.append(MC_price.pricingByMC())
#     QMC.append(QMC_price.pricingByQMC())
#     Xaxis.append(i*100)
#     print("times: " + str(i))
#
# for i in range(50):
#     MC_price = PricingBO_MC([157.41, 153.06, 195.69, 78.76, 12.27], 100, 0.0111, 0.25, 0.01, 1000, corr,
#                             [0.35, 0.3, 0.1, 0.1, 0.15], 0.219, 0.383, 0.155, 0.173,
#                             0.166)
#     QMC_price = PricingBO_QMC([157.41, 153.06, 195.69, 78.76, 12.27], 100, 0.0111, 0.25, 0.01, 1000, corr,
#                               [0.35, 0.3, 0.1, 0.1, 0.15], 0.219, 0.383, 0.155, 0.173,
#                               0.166)
#     QMC_price.generatePrimeInt()
#     QMC_price.generateHaltonSequences()
#     MC_price.setIteration(10000 + i * 200)
#     QMC_price.setIteration(10000 + i * 200)
#
#     MC.append(MC_price.pricingByMC())
#     QMC.append(QMC_price.pricingByQMC())
#     Xaxis.append(10000 + i * 200)
#     print("times: " + str(i))

for i in range(50):
    MC_price = PricingBO_MC([157.41, 153.06, 195.69, 78.76, 12.27], 100, 0.0111, 0.25, 0.01, 1000, corr,
                            [0.35, 0.3, 0.1, 0.1, 0.15], 0.219, 0.383, 0.155, 0.173,
                            0.166)
    QMC_price = PricingBO_QMC([157.41, 153.06, 195.69, 78.76, 12.27], 100, 0.0111, 0.25, 0.01, 1000, corr,
                              [0.35, 0.3, 0.1, 0.1, 0.15], 0.219, 0.383, 0.155, 0.173,
                              0.166)
    QMC_price.generatePrimeInt()
    QMC_price.generateHaltonSequences()
    MC_price.setIteration(20000 + i * 200)
    QMC_price.setIteration(20000 + i * 200)

    MC.append(MC_price.pricingByMC())
    QMC.append(QMC_price.pricingByQMC())
    Xaxis.append(30000 + i * 200)
    print("times: " + str(i))

plt.plot(Xaxis, MC, "r--", label = "Monte Carlo")
plt.plot(Xaxis, QMC, label = "Halton Quasi-Monte Carlo")
plt.xlabel("Number of iterations")
plt.ylabel("Price")
plt.ylim((np.mean(MC) + np.mean(QMC)) / 2 - 0.5, (np.mean(MC) + np.mean(QMC)) / 2 + 0.5)
plt.legend()
plt.show()
