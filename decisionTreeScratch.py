import pandas as pd
import scipy as sc
import numpy as np
import math
import decisionTree as dt

dt.buildTree("training_set_1.csv", "e")
#dt.buildTree("training_set_1.csv", "v")

# n = dt.node("asdf")
# n.total = 14
# n.mismatchesOne = 4
# n.matchesOne = 3
# n.mismatchesZero = 6
# n.matchesZero = 1
# print(n.gainVI())

def findEntropy(matches, mismatches):
    total = matches + mismatches
    print(total)
    first = -1 * (matches / total) * np.log2(matches / total)
    print(first)
    second = -1 * (mismatches / total) * np.log2(mismatches / total)
    print(second)
    return first + second