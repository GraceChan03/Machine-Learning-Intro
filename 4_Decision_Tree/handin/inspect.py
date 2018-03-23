import sys, math

def main(argv=None):
    arg = sys.argv
    file = str(arg[1])
    counter = dict()
    samples = 0
    with open(file, "r") as f:
        # name of attributes
        line = f.readline()
        while line:
            line = f.readline().rstrip('\n\r')
            # the last column is the class
            if line != '':
                cells = line.split(",")
                classification = cells[len(cells) - 1]
                if classification in counter:
                    counter[classification] += 1
                else:
                    counter[classification] = 1
                samples += 1
    entropy = 0.0
    max = 0.0
    for key in counter.keys():
        count = counter[key]
        rate = float(count)/samples
        if rate != 0:
            h = -float(rate) * math.log(rate, 2)
            entropy += h
        if count > max:
            max = float(count)
    sys.stdout.write("entropy: " + str(entropy) + "\n")
    error = 1 - max / samples
    sys.stdout.write("error: " + str(error))


if __name__ == "__main__" :
    main()