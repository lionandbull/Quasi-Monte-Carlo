import numpy as np
import pandas as pd
from prettytable import PrettyTable

class Correlation:
    def __init__(self, *files):
        self.files = files
        self.stocksPriceList = []
        self.returns = []
        self.weight = []
        self.stocksVolList = []
        self.returnsSquare = []
        self.volatility = []
        self.covariance = []
        self.corr = []

    ## lbd is lambda
    def setWeight(self, lbd):
        self.weight.append([1 - lbd])
        for i in range(len(self.stocksPriceList[0]) - 2):
            prev = self.weight[-1][0]
            self.weight.append([prev*lbd])

    def getPriceList(self):
        for i in self.files:
            csv = pd.read_csv(i)
            csv.drop(['Date', 'Open', 'High', 'Low', 'Adj Close', 'Volume'], axis=1, inplace=True)
            self.stocksPriceList.append(csv.as_matrix())

    def calReturns(self):
        for pricelist in self.stocksPriceList:
            singleReturn = []
            for i in range(len(pricelist)):
                if i == len(pricelist) - 1:
                    break
                singleReturn.append(np.log(pricelist[i + 1] / pricelist[i])[0])
            self.returns.append(singleReturn)



    def calReturnsSquare(self):
        for i in range(len(self.returns)):
            self.returnsSquare.append(np.asarray(self.returns[i])**2)

    def calVolatility(self):
        for i in range(len(self.files)):
            self.volatility.append(np.sum(np.asarray(self.returnsSquare[i]) *
                                   np.asarray(self.weight)))

        # for i in range(len(self.files)):
        #     sigma = 1
        #     for j in range(self.returnsSquare):
        #         sigma = 0.94 + 0.06*self.returnsSquare[i]
        #         self.volatility.append()

    def calCovariance(self):
        for i in range(len(self.files) - 1):
            covarianceList = []
            for j in range(i + 1, len(self.files)):
                returnX = np.asarray(self.returns[i])
                returnY = np.asarray(self.returns[j])
                covarianceList.append(np.sum(returnX * returnY * np.asarray(self.weight)))
            self.covariance.append(covarianceList)


    def calCorr(self):
        for i in range(len(self.files)):
            corrList = []
            for j in range(len(self.files)):
                if i == j:
                    corrList.append(1)
                elif i < j:
                    corrList.append(self.covariance[i][j - i - 1]/
                                     (np.sqrt(self.volatility[i]) * np.sqrt(self.volatility[j])))
                elif i > j:
                    corrList.append(self.corr[j][i])
            self.corr.append(corrList)

    def toMatrixForm(self):
        for row in self.corr:
            print(row)

    def printTable(self):
        x = PrettyTable(["Ticker", "AAPL", "IBM", "NVDA", "MSFT", "F"])
        x.align["Value"] = "l"
        x.padding_width = 1
        x.add_row(["AAPL",
                   self.corr[0][0],
                   self.corr[0][1],
                   self.corr[0][2],
                   self.corr[0][3],
                   self.corr[0][4]])
        x.add_row(["IBM",
                   self.corr[1][0],
                   self.corr[1][1],
                   self.corr[1][2],
                   self.corr[1][3],
                   self.corr[1][4]])
        x.add_row(["NVDA",
                   self.corr[2][0],
                   self.corr[2][1],
                   self.corr[2][2],
                   self.corr[2][3],
                   self.corr[2][4]])
        x.add_row(["MSFT",
                   self.corr[3][0],
                   self.corr[3][1],
                   self.corr[3][2],
                   self.corr[3][3],
                   self.corr[3][4]])
        x.add_row(["F",
                   self.corr[4][0],
                   self.corr[4][1],
                   self.corr[4][2],
                   self.corr[4][3],
                   self.corr[4][4]])

        print(x)



# test = Correlation('AAPL.csv', 'IBM.csv', 'NVDA.csv', 'MSFT.csv', 'F.csv')
# test.getPriceList()
# test.setWeight(0.94)
# test.calReturns()
# test.calReturnsSquare()
# test.calVolatility()
# test.calCovariance()
# test.calCorr()
# test.toMatrixForm()
# test.printTable()


# test = Correlation('test1.csv', 'test2.csv')
# test.getPriceList()
# test.setWeight(0.94)
# test.calReturns()
# test.calReturnsSquare()
# test.calVolatility()
# test.calCovariance()
# test.calCorr()
# print(test.corr)








