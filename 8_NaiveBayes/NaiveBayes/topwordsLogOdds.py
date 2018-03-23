from nb import NaiveBayes
import sys
from math import log
from itertools import islice

if __name__ == '__main__':
    nb = NaiveBayes(sys.argv[1])
    nb.calculate_p_wv()
    c_libs = len(nb.text_libs)
    c_cons = len(nb.text_cons)
    log_lib = dict()
    log_con = dict()
    for w, [p1, p2] in nb.p_wv.items():
        log_lib[w] = log(p1) - log(p2)
        log_con[w] = log(p2) - log(p1)
    for w in islice(sorted(log_lib, key=log_lib.get, reverse=True), 20):
        print(w + " %.04f" % log_lib[w])
    print
    for w in islice(sorted(log_con, key=log_con.get, reverse=True), 20):
        print(w + " %.04f" % log_con[w])
