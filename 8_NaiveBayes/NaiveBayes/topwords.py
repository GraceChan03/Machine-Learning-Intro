from nb import NaiveBayes
from itertools import islice
import sys

if __name__ == '__main__':
    nb = NaiveBayes(sys.argv[1])
    nb.calculate_p_wv()
    for w, p in islice(sorted(nb.p_wv.items(), key=lambda pair:pair[1][0], reverse=True), 20):
        print(w + " %.04f" % p[0])
    print
    for w, p in islice(sorted(nb.p_wv.items(), key=lambda pair:pair[1][1], reverse=True), 20):
        print(w + " %.04f" % p[1])
