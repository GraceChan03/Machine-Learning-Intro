from nb import NaiveBayes

class NBStopWords:
    def __init__(self, train_file, test_file, N):
        self.V = ['lib', 'con']
        self.test_file = test_file
        self.NB = NaiveBayes(train_file)
        self.N = N
        self.exclude_stopwords()
        self.NB.calculate_p_wv()
        self.test()

    def exclude(self, word, counter):
        if word in counter:
            del counter[word]

    def exclude_stopwords(self):
        stopwords = list()
        for word in self.NB.vocabulary.most_common(self.N):
            w = word[0]
            stopwords.append(w)
            self.exclude(w, self.NB.text_libs)
            self.exclude(w, self.NB.text_cons)
        for word in stopwords:
            self.exclude(word, self.NB.vocabulary)

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
    NBStopWords(sys.argv[1], sys.argv[2], int(sys.argv[3]))