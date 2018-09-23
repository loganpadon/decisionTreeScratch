import pandas as pd
import numpy as np
illegal = ["Class"]

class decisionTree:
    """"A class that represents a binary decision tree"""
    leadingNode = None

    def addNode(self, node):
        self.leadingNode = node


def entropy(matches, mismatches):
    total = matches + mismatches
    first = -1 * (matches / total) * np.log2(matches / total)
    second = -1 * (mismatches / total) * np.log2(mismatches / total)
    return first + second


def varianceImpurity(zeroes, ones):
    total = ones + zeroes
    first = ones / total
    second = zeroes / total
    return first * second


class node:
    zeroNode = None
    oneNode = None
    label = None
    leaf = False
    total = 0
    matches = 0
    mismatches = 0
    matchesZero = 0
    matchesOne = 0
    mismatchesZero = 0
    mismatchesOne = 0

    def __init__(self, label):
        self.label = label

    def addMatchZero(self):
        self.matchesZero = self.matchesZero+1
        self.matches = self.matches + 1
        self.total = self.total+1

    def addMatchOne(self):
        self.matchesOne = self.matchesOne + 1
        self.matches = self.matches + 1
        self.total = self.total + 1

    def addMismatchZero(self):
        self.mismatches = self.mismatches+1
        self.mismatchesZero = self.mismatchesZero + 1
        self.total = self.total+1

    def addMismatchOne(self):
        self.mismatches = self.mismatches+1
        self.mismatchesOne = self.mismatchesOne + 1
        self.total = self.total+1

    def gain(self):
        first = entropy(self.matchesOne+self.mismatchesZero, self.matchesZero+self.mismatchesOne)
        second = ((self.matchesOne+self.mismatchesOne)/self.total) * entropy(self.matchesOne, self.mismatchesOne)
        third = ((self.matchesZero+self.mismatchesZero)/self.total) * entropy(self.mismatchesZero, self.matchesZero)
        return first - second - third

    def gainVI(self):
        first = varianceImpurity(self.matchesOne + self.mismatchesZero, self.matchesZero + self.mismatchesOne)
        second = ((self.matchesOne+self.mismatchesOne)/self.total) * varianceImpurity(self.matchesOne, self.mismatchesOne)
        third = ((self.matchesZero + self.mismatchesZero) / self.total) * varianceImpurity(self.mismatchesZero, self.matchesZero)
        return first - second - third


def buildTree(trainingFileName, vOrE):
    best = node("")
    tf = pd.read_csv(trainingFileName)
    classCol = tf[['Class']]
    for key, value in tf.iteritems():
        if key not in illegal:
            i = 0
            n = node(key)
            for element in value:
                element = int(element)
                answer = int(classCol.values[i])
                if element == answer:
                    if element == 0:
                        n.addMatchZero()
                    else:
                        n.addMatchOne()
                else:
                    if element == 0:
                        n.addMismatchZero()
                    else:
                        n.addMismatchOne()
                i = i+1
        # print(n.label)
        # print(n.matches)
        # print(n.matchesZero)
        # print(n.matchesOne)
        # print(n.mismatches)
        # print(n.mismatchesZero)
        # print(n.mismatchesOne)
        # print(n.total)
        if vOrE == "e":
            if best.label == "":
                print(n.gain())
                best = n
            if best.gain() < n.gain():
                print(n.gain())
                best = n
        else:
            if best.label == "":
                print(n.gainVI())
                best = n
            if best.gain() < n.gain():
                print(n.gainVI())
                best = n

    illegal.append(best.label)
    print("root " + best.label)
    best.zeroNode = buildTreeHelper(trainingFileName, vOrE, best, 0)
    print("zn of " + best.label + " is " + best.zeroNode.label)
    best.oneNode = buildTreeHelper(trainingFileName, vOrE, best, 1)
    print("on of " + best.label + " is " + best.oneNode.label)

    dt = decisionTree()
    dt.addNode(best)
    return dt


def buildTreeHelper(trainingFileName, vOrE, n, zOrO):
    best = node("")
    tf = pd.read_csv(trainingFileName)
    classCol = tf[['Class']]
    parent = tf[[n.label]]
    for key, value in tf.iteritems():
        if key not in illegal:
            i = 0
            n = node(key)
            for element in value:
                element = int(element)
                answer = int(classCol.values[i])
                parentVal = int(parent.values[i])
                if parentVal == zOrO:
                    if element == answer:
                        if element == 0:
                            n.addMatchZero()
                        else:
                            n.addMatchOne()
                    else:
                        if element == 0:
                            n.addMismatchZero()
                        else:
                            n.addMismatchOne()
                i = i + 1
        # print(n.label)
        # print(n.matches)
        # print(n.matchesZero)
        # print(n.matchesOne)
        # print(n.mismatches)
        # print(n.mismatchesZero)
        # print(n.mismatchesOne)
        # print(n.total)
        if vOrE == "e":
            if best.label == "":
                print(n.gain())
                best = n
            if best.gain() < n.gain():
                print(n.gain())
                best = n
        else:
            if best.label == "":
                print(n.gainVI())
                best = n
            if best.gain() < n.gain():
                print(n.gainVI())
                best = n
    illegal.append(best.label)
    if len(illegal) == 20:
        return best
    return best
#todo figure out when something should be a leaf
#todo implement printing
#todo implement testing
#todo implement pruning
