from forward import HMM
from logsum import log_sum
from math import log
import sys

class Backward:
    def __init__(self, dev, trans_file, emit_file, prior_file):
        self.hmm = HMM(trans_file, emit_file, prior_file)
        self.dev_file = dev

    def handle_dev(self):
        with open(self.dev_file, 'r') as file:
            for line in file:
                words = line.rstrip('\n\r').split(" ")
                dev = list()
                T = len(words)
                t = T
                for i in range(len(words)):
                    if t == T:
                        beta_T = [log(1) for x in range(self.hmm.N)]
                        dev.append(beta_T)
                    else:
                        self.calculate_beta(dev, words[t], t - 1, T - 1)
                    t -= 1
                p = self.calculate_P(dev, words[0])
                print p


    def calculate_P(self, dev, o1):
        beta1 = dev[len(dev) - 1]
        p = 0.0
        for i in range(self.hmm.N):
            pii = log(self.hmm.pi[i])
            bi = log(self.hmm.b[o1][i])
            beta1_i = beta1[i]
            sum = pii + bi + beta1_i
            if i == 0:
                p = sum
            else:
                p = log_sum(p, sum)
        return p

    def calculate_beta(self, dev, o_tp1, t, T):
        beta_t = list()
        for i in range(self.hmm.N):
            beta_ti = 0.0
            for j in range(self.hmm.N):
                beta_tp1_j = dev[T - (t + 1)][j]
                a_ij = log(self.hmm.a[i][j])
                b_j = log(self.hmm.b[o_tp1][j])
                sum = beta_tp1_j + a_ij + b_j
                if j == 0:
                    beta_ti = sum
                else:
                    beta_ti = log_sum(beta_ti, sum)
            beta_t.append(beta_ti)
        dev.append(beta_t)

if __name__ == '__main__':
    b = Backward(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    b.handle_dev()