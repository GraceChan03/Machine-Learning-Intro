from forward import HMM
from math import log
import operator
import sys

class Viterbi:
    def __init__(self, dev, trans_file, emit_file, prior_file):
        self.hmm = HMM(trans_file, emit_file, prior_file)
        self.dev_file = dev
        self.handle_dev()

    def handle_dev(self):
        with open(self.dev_file, 'r') as file:
            for line in file:
                words = line.rstrip('\n\r').split(" ")
                vp = list()
                q = list()
                for i in range(len(words)):
                    t = i + 1
                    if t == 1:
                        self.initialize(vp, q, words[0])
                    else:
                        self.calculate(vp, q, words[i], i)
                Q = self.get_Q(vp, q)
                Q = Q.split("\t")
                tag = ""
                for i in range(len(words)):
                    tag += words[i] + "_" + Q[i] + " "
                tag = tag.rstrip(" ")
                print tag

    def get_Q(self, vp, q):
        vp_t = vp[len(vp) - 1]
        index, vp_t_max = max(enumerate(vp_t), key=operator.itemgetter(1))
        return q[len(q) - 1][index]

    def calculate(self, vp, q, o_tp1, t):
        vp_tp1 = list()
        q_tp1 = list()
        for i in range(self.hmm.N):
            vp_tp1_ = list()
            bi = log(self.hmm.b[o_tp1][i])
            for j in range(self.hmm.N):
                vp_t = vp[t - 1][j]
                a_ji = log(self.hmm.a[j][i])
                s = vp_t + a_ji + bi
                vp_tp1_.append(s)
            index, vp_tp1_i = max(enumerate(vp_tp1_), key=operator.itemgetter(1))
            vp_tp1.append(vp_tp1_i)
            q_tp1_i = q[t - 1][index] + "\t" + self.hmm.symbols[i]
            q_tp1.append(q_tp1_i)
        vp.append(vp_tp1)
        q.append(q_tp1)


    def initialize(self, vp, q, o1):
        vp1 = list()
        for i in range(self.hmm.N):
            pii = log(self.hmm.pi[i])
            bi = log(self.hmm.b[o1][i])
            vpi = pii + bi
            vp1.append(vpi)
        vp.append(vp1)
        q.append(self.hmm.symbols)

if __name__ == '__main__':
    v = Viterbi(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])