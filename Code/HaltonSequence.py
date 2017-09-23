import numpy as np
import matplotlib.pyplot as plt

class Halton_Sequence:
    def __init__(self, iterations, base):
        self.iterations = iterations
        self.b = base

    def BExpansion(self, k):
        if (k > 0):
            j_max = np.floor(np.log(k) / np.log(self.b))
            ## define a coefficient array named with coe
            coe = np.zeros(int(j_max) + 1)
            q = self.b ** j_max
            for j in range(0, int(j_max) + 1):
                coe[j] = np.floor(k / q)
                k = k - q * coe[j]
                q = q / self.b
        return coe

    def nextBExpansion(self, coe_first):
        m = len(coe_first)
        coe_next = np.zeros(m + 1)
        carry = True
        for i in range(0, m):
            if carry:
                if (coe_first[m - 1 - i] == self.b - 1):
                    coe_next[m - i] = 0
                else:
                    coe_next[m - i] = coe_first[m - 1 - i] + 1
                    carry = False
            else:
                coe_next[m - i] = coe_first[m - 1 - i]
        if carry:
            coe_next[0] = 1
        return coe_next

    def getSequence(self, coe_list):
        m = len(coe_list)
        sequence = []
        for n in range(m):
            coe_length = len(coe_list[n])
            x = 0
            q = 1 / self.b
            for i in range(1, coe_length + 1):
                x = x + q * coe_list[n][coe_length - i]
                q = q / self.b
            sequence.append(x)
        return sequence

    def returnSequence(self):
        list = []
        list.append(np.array([0]))
        list.append(self.BExpansion(1))
        for i in range(self.iterations - 1):
            list.append(self.nextBExpansion(list[i + 1]))
        sequence = self.getSequence(list)

        return sequence

# iterations = 2000
# sequence1 = Halton_Sequence(iterations, 2)
# print(sequence1.returnSequence())
#sequence2 = Halton_Sequence(iterations, 3)
#print(sequence2.returnSequence())
#plt.plot(sequence1.returnSequence(), sequence2.returnSequence(), 'ro')
#plt.hlines(0.84, 0, 0.5, colors='k')
#plt.vlines(0.5, 0.84, 1, colors='k')
#plt.annotate('No points in this region', xy=(0.1, 0.88), xytext=(0.15, 0.94),
#            arrowprops=dict(facecolor='black', shrink=0.05))
#plt.xlabel('')
#plt.ylabel('')
# plt.title('First ' + str(iterations) + ' points of two-dimensional Halton sequence with base 2 and 3.')
#plt.show()




# iterations = 2000
# sequence1 = Halton_Sequence(iterations, 2)
# sequence2 = Halton_Sequence(iterations, 3)
# plt.plot(sequence1.returnSequence(), sequence2.returnSequence(), 'ro')
# plt.show()







