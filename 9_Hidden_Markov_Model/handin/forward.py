from logsum import log_sum
from math import log
import sys

class HMM:
    def __init__(self, trans_file, emit_file, prior_file):
        self.a = list()
        self.symbols = list()
        self.init_trans(trans_file)
        self.N = len(self.a)
        self.b = dict()
        self.init_emit(emit_file)
        self.pi = list()
        self.init_prior(prior_file)

    def init_trans(self, trans_file):
        with open(trans_file, 'r') as file:
            for line in file:
                labels = line.rstrip('\n\r ').split(" ")
                labels_num = len(labels) - 1
                prob = list()
                for i in range(labels_num):
                    lp = labels[i + 1].split(":")
                    prob.append(float(lp[1]))
                self.a.append(prob)

    def init_emit(self, emit_file):
        with open(emit_file, 'r') as file:
            label = 0
            for line in file:
                words = line.rstrip('\n\r ').split(" ")
                words_num = len(words) - 1
                for i in range(words_num):
                    wp = words[i + 1].split(":")
                    w = wp[0]
                    p = float(wp[1])
                    if w in self.b:
                        self.b[w][label] = p
                    else:
                        self.b[w] = [0.0 for i in range(self.N)]
                        self.b[w][label] = p
                label += 1

    def init_prior(self, prior_file):
        with open(prior_file, 'r') as file:
            for line in file:
                lp = line.rstrip('\n\r').split(" ")
                self.pi.append(float(lp[1]))
                self.symbols.append(lp[0])

class Forward:
    def __init__(self, dev, trans_file, emit_file, prior_file):
        self.hmm = HMM(trans_file, emit_file, prior_file)
        # t is from [1, T); n is from [0, N)
        self.dev_file = dev

    def handle_dev(self):
        with open(self.dev_file, 'r') as file:
            for line in file:
                words = line.rstrip('\n\r').split(" ")
                dev = list()
                # calculate conditional probability
                for i in range(len(words)):
                    t = i + 1
                    if t == 1:
                        self.initialize_alpha(words[0], dev)
                    else:
                        self.calculate_alpha(words[i], t, dev)
                print self.calculate_P(dev)

    def calculate_P(self, dev):
        T = len(dev)
        alpha_T = dev[T - 1]
        sum = 0.0
        for i in range(len(alpha_T)):
            if i == 0:
                sum = alpha_T[0]
            else:
                sum = log_sum(sum, alpha_T[i])
        return sum

    def calculate_alpha(self, o_tp1, tp1, dev):
        alpha_tp1 = list()
        for i in range(self.hmm.N):
            bi = log(self.hmm.b[o_tp1][i])
            logsum = 0.0
            for j in range(self.hmm.N):
                a_tj = dev[tp1 - 2][j]
                a_ji = log(self.hmm.a[j][i])
                sum = a_tj + a_ji
                if j == 0:
                    logsum = sum
                else:
                    logsum = log_sum(logsum, sum)
            alpha_tp1_i = bi + logsum
            alpha_tp1.append(alpha_tp1_i)
        dev.append(alpha_tp1)


    def initialize_alpha(self, o1, dev):
        alpha1 = list()
        for i in range(self.hmm.N):
            pii = log(self.hmm.pi[i])
            bi = log(self.hmm.b[o1][i])
            alpha_i = pii + bi
            alpha1.append(alpha_i)
        dev.append(alpha1)


if __name__ == '__main__':
    f = Forward(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    f.handle_dev()