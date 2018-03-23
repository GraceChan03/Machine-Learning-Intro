import random
import numpy as np
import numpy.random as random
import math
import time
import sys

t0 = time.time()

def normalize(attr_file, key_file=None):
    attr_arr = list()
    with open(attr_file, "r") as f:
        attr_name = [x.strip() for x in f.readline().rstrip('\n').split(',')]
        line = f.readline().rstrip('\n\r')
        while line:
            attrs = line.split(',')
            attrs[0] = float(2000 - float(attrs[0]))/ 50 - 1
            attrs[1] = float(7 - float(attrs[1]))/3.5 - 1
            if attrs[2] == 'yes':
                attrs[2] = 1
            else:
                attrs[2] = -1
            if attrs[3] == 'yes':
                attrs[3] = 1
            else:
                attrs[3] = -1
            # bias
            attrs.append(1.0)
            attr_arr.append(attrs)
            line = f.readline().rstrip('\n\r')
    attr_np = np.array(attr_arr)
    if key_file is None:
        return attr_np
    key_arr = list()
    with open(key_file, "r") as f:
        for line in f:
            key = line.rstrip('\n\r')
            if key == 'yes':
                key_arr.append(1)
            else:
                key_arr.append(0)
    label_np = np.array(key_arr)
    label_np = label_np.reshape((label_np.size, 1))
    sample = np.hstack((attr_np, label_np))
    return sample

def sigmoid(net):
    return 1.0/(1.0 + math.exp(0.0 - net))

# n_h - number of hidden unit
def BP(sample, lr, n_h):
    # number of input unit
    n_in = sample[0].size - 1
    # initialize hidden w
    hid_w = random.uniform(-0.05, 0.05, (n_h, n_in))
    # initialize output, the final unit from hidden is bias
    out_w = random.uniform(-0.05, 0.05, n_h + 1)
    # until the termination condition is met
    count = 0
    delta_time = time.time() - t0
    while delta_time < 30:
        error = 0.0
        count += 1
        delta_time = time.time() - t0
        random.shuffle(sample)
        for i in range(sample.shape[0]):
            x = sample[i][:n_in]
            t = sample[i][n_in]
            # use sigmoid to calculate output
            hid_o = np.dot(hid_w, x)
            for j in range(n_h):
                hid_o[j] = sigmoid(hid_o[j])
            hid_o = np.hstack((hid_o, [1])) #shape(3,)
            out_o = np.dot(out_w, hid_o)
            # only one output unit
            out_o = sigmoid(out_o)
            error += (t - out_o)**2
            # error term of output unit - delta
            out_d = out_o * (1 - out_o) * (t - out_o)
            # error term of each hidden unit h, including bias
            hid_d = hid_o * (1 - hid_o) * out_w * out_d
            out_w += lr * out_d * hid_o
            for k in range(n_h):
                hid_w[k] += lr * hid_d[k] * x
        if count%100 == 0:
            print(error)
    print(count)
    return hid_w, out_w

def predict(dev, hid_w, out_w):
    for i in range(dev.shape[0]):
        x = dev[i]
        hid_o = np.dot(hid_w, x)
        n_h = hid_w.shape[0]
        for j in range(n_h):
            hid_o[j] = sigmoid(hid_o[j])
        hid_o = np.hstack((hid_o, [1]))
        out_o = np.dot(out_w, hid_o)
        out_o = sigmoid(out_o)
        if out_o > 0.5:
            print('yes')
        else:
            print('no')

# def handler(label_file):
#     label = list()
#     with open(label_file, "r") as f:
#         for line in f:
#             key = line.rstrip('\n\r')
#             label.append(key)
#     return np.array(label)

def main():
    arg = sys.argv
    sample = normalize(arg[1], arg[2])
    hid_w, out_w = BP(sample, 0.05, 4)
    print("TRAINING COMPLETED! NOW PREDICTING.")
    dev = normalize(arg[3])
    predict(dev, hid_w, out_w)

if __name__ == '__main__':
    main()