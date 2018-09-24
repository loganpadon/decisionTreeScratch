import pandas as pd
import scipy as sc
import numpy as np
import math
import decisionTree as dt
import sys

tree = dt.buildTree("training_set_1.csv", "e")
tree.printTree()
tree = dt.buildTree("training_set_1.csv", "v")
tree.printTree()
print(tree.test("test_set_1.csv"))
#dt.buildTree("training_set_1.csv", "v")

def findEntropy(matches, mismatches):
    total = matches + mismatches
    print(total)
    first = -1 * (matches / total) * np.log2(matches / total)
    print(first)
    second = -1 * (mismatches / total) * np.log2(mismatches / total)
    print(second)
    return first + second

# n = dt.node("asdf")
# n.total = 4
# n.mismatchesOne = 4
# n.matchesOne = 0
# n.mismatchesZero = 0
# n.matchesZero = 0
# print(findEntropy(n.matchesOne, n.mismatchesOne))

def __main_(): #todo to make this real, add an extra _ at the end of the name
    l = sys.argv[0]
    k = sys.argv[1]
    trainingSet = sys.argv[2]
    validationSet = sys.argv[3]
    testSet = sys.argv[4]
    toPrint = sys.argv[5]
    tree = dt.buildTree(trainingSet, "e")
    print("Test results, entropy: " + tree.test(testSet))
    print("Test results, post pruning, entropy" + dt.postPruning(tree, l, k, validationSet))
    if toPrint == "yes":
        tree.printTree()

    tree = dt.buildTree(trainingSet, "v")
    print("Test results, VI: " + tree.test(testSet))
    print("Test results, post pruning, VI" + dt.postPruning(tree, l, k, validationSet))
    if toPrint == "yes":
        tree.printTree()




