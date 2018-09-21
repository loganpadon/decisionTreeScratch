import pandas as pd
import scipy as sc
import numpy as np
import math

def findEntropy(labels, base=None):
    value,counts = np.unique(labels, return_counts=True)
    return entropy(counts, base=base)