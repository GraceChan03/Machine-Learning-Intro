import sys, math

class Node:
    def __init__(self, positive=0, negative=0, attr=-1, label=0):
        self.left = None
        self.right = None
        self.entropy = 0
        self.mutual_information = 0
        self.positive = positive
        self.negative = negative
        # the index of attribute decides the following path
        self.decision_attr = -1
        # 0 or 1 -> no or yes
        self.label = label
        # remember the attribute of current node
        self.attr = attr

positive_labels = ['democrat', 'y', 'A', 'yes', 'before1950', 'morethan3min', 'fast', 'expensive', 'high', 'Two', 'morethan3min', 'large']
def inputHandler(file):
    with open(file, "r") as f:
        attr_name = [x.strip() for x in f.readline().rstrip('\n').split(',')]
        line = f.readline().rstrip('\n\r')
        attr_val = list()
        while line:
            cells = line.split(',')
            attr_val.append([1 if x in positive_labels else 0 for x in cells])
            line = f.readline().rstrip('\n\r')
    return attr_name, attr_val


def entropy(positive_rate):
    negative_rate = 1 - positive_rate
    if positive_rate == 0.0 or negative_rate == 0.0:
        return 0.0
    entropy = -(float(positive_rate) * math.log(positive_rate, 2) + float(negative_rate) * math.log(negative_rate, 2))
    return entropy

def calEntropy(array):
    sum = 0
    for x in array:
        sum += x
    if sum == 0 or sum == len(array):
        return 0
    positive_rate = float(sum)/len(array)
    return entropy(positive_rate)

def getBestAttr(Examples, Attributes, root):
    entropy = root.entropy
    mis = []
    for attr in Attributes:
        p = []
        n = []
        for e in Examples:
            if e[attr] == 0:
                n.append(e[-1])
            else:
                p.append(e[-1])
        attr_e = entropy - float(len(p))/len(Examples)*calEntropy(p) - float(len(n))/len(Examples)*calEntropy(n)
        mis.append(attr_e)
    root.mutual_information = max(mis)
    return Attributes[mis.index(max(mis))]

def ID3(Examples, Target_attribute, Attributes, depth):
    if depth > 2:
        return
    positive = 0
    total_nodes = len(Examples)
    for e in Examples:
        positive += 1 if e[-1] == 1 else 0
    # the tree only has one node
    root = Node(positive=positive, negative=total_nodes - positive, attr=Target_attribute)
    # if examples are all positive, return single-node tree with label = +
    if positive == total_nodes:
        root.label = 1
        return root
    # if examples are all negative, return single-node tree with label = -
    if positive == 0:
        root.label = 0
        return root

    # if Attributes is null, return sigle-node tree with label = popular Target_attribute
    root.entropy = entropy(float(positive) / total_nodes)
    root.label = 0 if positive < float(total_nodes) / 2 else 1
    if len(Attributes) == 0:
        return root

    # A <- the attribute from Attributes that best classifies Examples
    A = getBestAttr(Examples, Attributes, root)
    # The decision attribute for Root <- A
    root.decision_attr = A
    # use left to represent negative and right as positive
    # Let Examples(vi), be the subset of Examples that have value vi for A
    left_example = []
    right_example = []
    for e in Examples:
        if e[A] == 0:
            left_example.append(e)
        else:
            right_example.append(e)
    # if examples(vi) is null
    if len(left_example) == 0:
        root.label = 0 if positive < float(total_nodes) / 2 else 1
        return root
    if len(right_example) == 0:
        root.label = 0 if positive < float(total_nodes) / 2 else 1
        return root
    new_Attributes = [x for x in Attributes if x != A]
    # only split on an attribute if the mutual information is >= 0.1
    if root.mutual_information >= 0.1:
        root.left = ID3(left_example, A, new_Attributes, depth + 1)
        root.right = ID3(right_example, A, new_Attributes, depth + 1)
    return root

def printTree(root, depth, attr_name, right=True):
    if root is None or depth > 2:
        return
    if depth == 0:
        sys.stdout.write("[" + str(root.positive) + "+/" + str(root.negative) + "-]" + "\n")
    else:
        output = ""
        if depth > 1:
            output += "| "
        if right:
            output += attr_name[root.attr] + " = y: [" + str(root.positive) + "+/" + str(root.negative) + "-]"
        else:
            output += attr_name[root.attr] + " = n: [" + str(root.positive) + "+/" + str(root.negative) + "-]"
        sys.stdout.write(output + "\n")
    printTree(root.right, depth + 1, attr_name)
    printTree(root.left, depth + 1, attr_name, right=False)

def predict(root, data, depth, label):
    if root == None or depth > 2:
        return label
    # if depth == 2:
    #     return root.label
    if data[root.decision_attr] == 1:
        return predict(root.right, data, depth + 1, root.label)
    else:
        return predict(root.left, data, depth + 1, root.label)

def error(root, dataset):
    errors = 0
    for d in dataset:
        result = predict(root, d, depth=0, label=-1)
        if result != d[-1]:
            errors += 1
            # debug
            # print("error " + str(errors) + " | line" + str(index) + " " + str(d))
    return float(errors)

def main():
    arg = sys.argv
    train_file = str(arg[1])
    test_file = str(arg[2])
    # train_file = "../hw4data/politicians_train.csv"
    # test_file = "../hw4data/politicians_test.csv"
    train_attr_name, train_attr_val = inputHandler(train_file)
    root = ID3(train_attr_val, -1, [x for x in range(len(train_attr_name) - 1)], depth=0)
    printTree(root, 0, train_attr_name)
    # errors
    train_errors = float(error(root, train_attr_val))/len(train_attr_val)
    sys.stdout.write("error(train): " + str(train_errors) + "\n")
    test_attr_name, test_attr_val = inputHandler(test_file)
    test_errors = float(error(root, test_attr_val))/len(test_attr_val)
    sys.stdout.write("error(test): " + str(test_errors))

if __name__ == "__main__" :
    main()