from forward import HMM, Forward
from backward import Backward
from math import log
from logsum import log_sum

f = Forward("dev.txt", "hmm-trans.txt", "hmm-emit.txt", "hmm-prior.txt")
b = Backward("dev.txt", "hmm-trans.txt", "hmm-emit.txt", "hmm-prior.txt")
dev_file = "dev.txt"

with open(dev_file, 'r') as file:
    for line in file:
        words = line.rstrip('\n\r').split(" ")
        dev_a = list()
        dev_b = list()
        # calculate conditional probability
        for i in range(len(words)):
            t = i + 1
            if t == 1:
                f.initialize_alpha(words[0], dev_a)
            else:
                f.calculate_alpha(words[i], t, dev_a)
        T = len(words)
        t = T
        for i in range(len(words)):
            if t == T:
                beta_T = [log(1) for x in range(b.hmm.N)]
                dev_b.append(beta_T)
            else:
                b.calculate_beta(dev_b, words[t], t - 1, T - 1)
            t -= 1

        alpha5 = dev_a[4]
        beta5 = dev_b[len(dev_b) - 5]
        sum = 0.0
        for i in range(8):
            print alpha5[i] - beta5[i]