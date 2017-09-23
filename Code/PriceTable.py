from Correlation import Correlation
from BasketOption_QMC import PricingBO_QMC
from BasketOption_MC import PricingBO_MC
from prettytable import PrettyTable


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
    a = PricingBO_QMC(100, K, 0.0219, 0.15, 0.01, 5000, corr, [0.35, 0.3, 0.1, 0.1, 0.15], 0.227, 0.381, 0.159,
                        0.202, 0.171)
    a.generatePrimeInt()
    a.generateHaltonSequences()
    return a.pricingByQMC()

def auxiliaryFucMC(K):
    a = PricingBO_MC(100, K, 0.0219, 0.15, 0.01, 5000, corr, [0.35, 0.3, 0.1, 0.1, 0.15], 0.227, 0.381, 0.159,
                      0.202, 0.171)
    return a.pricingByMC()



x = PrettyTable(["Value", "K = 50", "K = 60", "K = 70", "K = 80", "K = 90", "K = 100", "K = 110", "K = 120"])
x.align["Value"] = "l"
x.padding_width = 1
x.add_row(["Quasi-Monte-Carlo",
           auxiliaryFucQMC(50),
           auxiliaryFucQMC(60),
           auxiliaryFucQMC(70),
           auxiliaryFucQMC(80),
           auxiliaryFucQMC(90),
           auxiliaryFucQMC(100),
           auxiliaryFucQMC(110),
           auxiliaryFucQMC(120)])
x.add_row(["Monte-Carlo",
           auxiliaryFucMC(50),
           auxiliaryFucMC(60),
           auxiliaryFucMC(70),
           auxiliaryFucMC(80),
           auxiliaryFucMC(90),
           auxiliaryFucMC(100),
           auxiliaryFucMC(110),
           auxiliaryFucMC(120)])

print(x)