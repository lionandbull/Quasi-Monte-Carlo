import numpy as np
import matplotlib.pyplot as plt

class PricingBO_MC:
    def __init__(self, S0, K, r, T, dt, iteration, corr, propCoef, *ImpliedVolatility):
        self.S0 = S0
        self.K = K
        self.S = []
        self.r = r
        self.T = T
        self.IV = ImpliedVolatility
        self.CorrRV = []
        self.BM = []
        self.corr = corr
        self.propCoef = propCoef
        self.iterations = int(T / dt) ## For generating sequence
        self.iteration = iteration  ## For generating asset paths
        self.dt = dt
        self.NDSeq = []
        #self.Xaxis = []
        #self.Yaxis = []

    def setIteration(self, iteration):
        self.iteration = iteration

    def generateBM(self):
        self.BM = []
        sigmaMatrix = [[self.IV[0], 0, 0, 0, 0],
                       [0, self.IV[1], 0, 0, 0],
                       [0, 0, self.IV[2], 0, 0],
                       [0, 0, 0, self.IV[3], 0],
                       [0, 0, 0, 0, self.IV[4]]]
        Sigma = np.dot(np.asarray(sigmaMatrix), np.asarray(self.corr))
        Sigma = np.dot(Sigma, np.asarray(sigmaMatrix))
        A = np.linalg.cholesky(Sigma)

        self.NDSeq = []
        for i in range(len(self.IV)):
            self.NDSeq.append(np.random.standard_normal(size=self.iterations))

        self.CorrRV = np.dot(A, np.asarray(self.NDSeq))

        for i in range(len(self.IV)):
            self.BM.append(np.cumsum(self.CorrRV[i]))
            self.BM[i] = np.hstack((np.array([0]), self.BM[i]))

    def pricingByMC(self):
        self.Xaxis = np.arange(0, self.T, self.dt)
        self.Xaxis = np.hstack((self.Xaxis, np.array([self.T])))
        V = []
        for n in range(self.iteration):
            self.S = []
            self.generateBM()
            S_T = []
            for i in range(len(self.IV)):
                p1 = (self.r - (self.IV[i] ** 2) / 2) * self.Xaxis
                p2 = self.IV[i] * np.sqrt(self.dt) * self.BM[i]
                self.S.append(self.S0[i] * np.exp(p1 + p2))
                #self.Yaxis.append(self.S)
                S_T.append(self.S[i][-1])
            payoff = max(np.sum(np.asarray(S_T) * np.asarray(self.propCoef)) - self.K, 0)
            V.append(payoff)
        price = np.exp(-self.r * self.T) * np.sum(V) / self.iteration
        return price

    # def plot_FourAssetsOnce(self, n):
    #     for i in range(len(self.IV)):
    #         plt.plot(self.Xaxis, self.Yaxis[n][i])
    #     plt.show()
    #
    # def plot_oneAssetNtimes(self, asset, N):
    #     if N > self.iteration:
    #         print("N should be less or equal to the parameter 'iteration' !")
    #     else:
    #         number = 0
    #         if asset == "AAPL":
    #             number = 0
    #         elif asset == "IBM":
    #             number = 1
    #         elif asset == "NVDA":
    #             number = 2
    #         elif asset == "MSFT":
    #             number = 3
    #         elif asset == "F":
    #             number = 4
    #
    #         for n in range(N):
    #             plt.plot(self.Xaxis, self.Yaxis[n][number])
    #         plt.show()


##generate corr matrix

# corrMatrix = Correlation('AAPL.csv', 'IBM.csv', 'NVDA.csv', 'MSFT.csv', 'F.csv')
# corrMatrix.getPriceList()
# corrMatrix.setWeight(0.94)
# corrMatrix.calReturns()
# corrMatrix.calReturnsSquare()
# corrMatrix.calVolatility()
# corrMatrix.calCovariance()
# corrMatrix.calCorr()
# corr = corrMatrix.corr


##pricing basket option by MC


