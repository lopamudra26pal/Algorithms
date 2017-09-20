import numpy as np
import random
import matplotlib.pyplot as plt
from collections import Counter

def ReservoirSampling(n):
    index = None
    i = 0
    while True:
        i = i+1
        if i>n:
            break
        if i == 1:
            index = 1
        else:
            index = np.random.choice([index,i],1,p=[1-1./i, 1./i])[0]
    return index

if __name__ == "__main__":
    n = 100
    items = []
    result = ReservoirSampling(n)
    #print result
    trials = [1000,10000,100000]

    for i in trials:
        for _ in range(i):
            result = ReservoirSampling(n)
            items.append(result)
        #count = [[x,items.count(x)] for x in items]

        count = Counter(items)
        print count
        # temp = []
        # dictlist = []
        # for key, value in count.items():
        #     aKey = key
        #     aValue = value
        #     temp.append(aKey)
        #     temp.append(aValue)
        #     dictlist.append(temp)
        #     aKey = 0
        #     aValue = 0
        #     temp = []
        # print dictlist

        plt.figure(i, figsize=(20,20))
        #plt.hist(dictlist, n)

        plt.bar(count.keys(), count.values(), color = 'blue')
        plt.xlabel("Items")
        plt.ylabel("Count")
        plt.title("Reservoir Sampling")
        plt.xlim(xmin=2,xmax=100)
        yint = []
        locs, labels = plt.yticks()
        for each in locs:
            yint.append(int(each))
        plt.yticks(yint)

        plt.savefig(str(i) + ".pdf")
        #plt.show()
        items = []

