import math
from collections import Counter

class NaiveBayes:
    def __init__(self, examples, q=1):
        self.V = ['lib', 'con']
        self.examples = examples
        self.vocabulary = Counter()
        self.text_libs = Counter()
        self.text_cons = Counter()
        self.p_lib = 0.0
        self.p_con = 0.0
        self.p_wv = dict()
        self.q = q
        self.collect(self.examples)

    def collect(self, examples):
        libs = 0.0
        cons = 0.0
        with open(examples, "r") as docs:
            for file in docs:
                # REMEMBER TO DELETE!!!!!!!
                file = file.rstrip('\n\r')
                if self.V[0] in file:
                    libs += 1
                    label = self.V[0]
                else:
                    cons += 1
                    label = self.V[1]
                words = list()
                with open(file, "r") as text:
                    for word in text:
                        word = word.lower().rstrip('\n\r')
                        words.append(word)
                    self.vocabulary.update(words)
                    if label == self.V[0]:
                        # add word into dictionary of lib
                        self.text_libs.update(words)
                    else:
                        self.text_cons.update(words)
        sum = libs + cons
        self.p_lib = float(libs) / sum
        self.p_con = float(cons) / sum


    def conditional_probability(self, n_k, n, voc_abs):
        return float(n_k + self.q) / (n + self.q * voc_abs)

    def calculate_p_wv(self):
        n_libs = sum(self.text_libs.values())
        n_cons = sum(self.text_cons.values())
        # a dict store conditional probability for each word: w -> [p(w|lib), p(w|con)]
        for w in self.vocabulary:
            p_lib = self.conditional_probability(self.text_libs.get(w, 0.0), n_libs, len(self.vocabulary))
            p_con = self.conditional_probability(self.text_cons.get(w, 0.0), n_cons, len(self.vocabulary))
            self.p_wv[w] = [p_lib, p_con]


    def classify(self, text):
        v_lib = 0.0
        v_con = 0.0
        for word in text:
            word = word.lower().rstrip("\n\r")
            if word not in self.vocabulary:
                continue
            v_lib += math.log(self.p_wv[word][0])
            v_con += math.log(self.p_wv[word][1])
        v_lib += math.log(self.p_lib)
        v_con += math.log(self.p_con)
        return v_lib, v_con

class NB:
    def __init__(self, train_file, test_file, q=1):
        self.V = ['lib', 'con']
        self.test_file = test_file
        self.NB = NaiveBayes(train_file, q)
        self.NB.calculate_p_wv()
        self.test()

    def test(self):
        accurate = 0
        sum = 0
        with open(self.test_file, "r") as docs:
            for doc in docs:
                sum += 1
                doc = doc.rstrip("\n\r")
                if self.V[0] in doc:
                    label = self.V[0]
                else:
                    label = self.V[1]
                with open(doc, "r") as text:
                    v_lib, v_con = self.NB.classify(text)
                if v_lib > v_con:
                    v_nb = self.V[0]
                    print "L"
                else:
                    v_nb = self.V[1]
                    print "C"
                if v_nb == label:
                    accurate += 1
        accuracy = float(accurate) / sum
        print("Accuracy: %.04f" % accuracy)


import sys

if __name__ == '__main__':
    NB("split.train", "split.test")