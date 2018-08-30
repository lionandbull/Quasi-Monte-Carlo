from HaltonSequence import Halton_Sequence
from Correlation import Correlation
import numpy as np
import matplotlib.pyplot as plt
import timeit




class PricingBO_QMC:
    def __init__(self, S0, K, r, T, dt, iteration, corr, propCoef, *ImpliedVolatility):
        self.S0 = S0
        self.K = K
        self.S = []
        self.r = r
        self.T = T
        self.IV = ImpliedVolatility
        self.primeInt = []
        self.randSeq = []
        self.NDSeq = []
        self.CorrRV = []
        self.BM = []
        self.corr = corr
        self.propCoef = propCoef
        self.iterations = int(T / dt) ## For generating sequence
        self.iteration = iteration ## For generating asset paths
        self.dt = dt
        #self.Xaxis = []
        #self.Yaxis = []

    def generatePrimeInt(self):
        for num in range(2, 100):
            if len(self.primeInt) == len(self.IV):
                break
            else:
                for j in range(2, num):
                    if (num % j) == 0:
                        break
                else:
                    self.primeInt.append(num)

    def setIteration(self, iteration):
        self.iteration = iteration

    def generateHaltonSequences(self):
        for i in range(len(self.IV)):
            self.randSeq.append(Halton_Sequence(self.iterations - 1, self.primeInt[i]).returnSequence())

    def randomShift(self):
        for num in range(len(self.IV)):
            self.randSeq[num] = (np.asarray(self.randSeq[num]) + np.random.uniform()) % 1


    def generateNDSeq(self):
        self.NDSeq = []
        a = [2.50662823884, -18.61500062529, 41.39119773534, -25.44106049637]
        b = [-8.4735109309, 23.08336743743, -21.06224101826, 3.13082909833]
        c = [0.3374754822726147, 0.9761690190917186, 0.1607979714918209, 0.0276438810333863,
             0.0038405729373609, 0.0003951896511919, 0.0000321767881768, 0.0000002888167364,
             0.0000003960315187]
        for num in range(len(self.IV)):
            self.NDSeq.append([])

        for i in range(len(self.IV)):
            for j in self.randSeq[i]:
                x = j - 0.5
                if abs(x) < 0.42:
                    y = x * x
                    self.NDSeq[i].append(
                        x * (((a[3] * y + a[2]) * y + a[1]) * y + a[0])
                        /
                        ((((b[3] * y + b[2]) * y + b[1]) * y + b[0]) * y + 1)
                    )
                else:
                    r = j
                    if x > 0:
                        r = 1 - j
                    if r == 0:
                        r = 0
                    else:
                        r = np.log(-np.log(r))
                    if x >= 0:
                        self.NDSeq[i].append(
                            c[0] + r * (c[1] + r * (c[2] + r * (c[3] + r * (c[4] + r * (c[5] + r * (c[6] +
                                                                                                    r * (c[7] + r * c[
                                                                                                        8])))))))
                        )

                    else:
                        self.NDSeq[i].append(-(
                            c[0] + r * (c[1] + r * (c[2] + r * (c[3] + r * (c[4] + r * (c[5] + r * (c[6] +
                                                                                                    r * (c[7] + r * c[
                                                                                                        8])))))))
                        ))

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

        self.CorrRV = np.dot(A, np.asarray(self.NDSeq))

        for i in range(len(self.IV)):
            self.BM.append(np.cumsum(self.CorrRV[i]))
            self.BM[i] = np.hstack((np.array([0]), self.BM[i]))

    def pricingByQMC(self):
        self.Xaxis = np.arange(0, self.T, self.dt)
        self.Xaxis = np.hstack((self.Xaxis, np.array([self.T])))

        V = []
        for n in range(self.iteration):
            #print("running...")
            self.S = []
            self.randomShift()
            self.generateNDSeq()
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

    # def plot_FiveAssetsOnce(self, n):
    #     print(self.Yaxis)
    #     for i in range(len(self.IV)):
    #         plt.plot(self.Xaxis, self.Yaxis[n][i])
    #     print(len(self.Xaxis), len(self.Yaxis[0]))
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



# #generate corr matrix
#
# corrMatrix = Correlation('AAPL.csv', 'IBM.csv', 'NVDA.csv', 'MSFT.csv', 'F.csv')
# corrMatrix.getPriceList()
# corrMatrix.setWeight(0.94)
# corrMatrix.calReturns()
# corrMatrix.calReturnsSquare()
# corrMatrix.calVolatility()
# corrMatrix.calCovariance()
# corrMatrix.calCorr()
# corr = corrMatrix.corr
#
# #pricing basket option by QMC
#
# basketOption = PricingBO_QMC([157.41, 153.06, 195.69, 78.76, 12.27], 120, 0.0111, 0.25, 0.01, 1000, corr, [0.35, 0.3, 0.1, 0.1, 0.15], 0.219, 0.383, 0.155, 0.173,
#                                 0.166)
# basketOption.generatePrimeInt()
# basketOption.generateHaltonSequences()
# basketOption.setIteration(5000)
# basketOption.pricingByQMC()












