import pandas as pd
import numpy as np
import random as rd
illegal = ["Class"]

class decisionTree:
    """"A class that represents a binary decision tree"""
    leadingNode = None
    nodeArray = []

    def addNode(self, node):
        self.leadingNode = node

    def printTree(self):
        pipelines = 0
        zero = self.leadingNode.label + " = 0 :"
        if self.leadingNode.leafZero and self.leadingNode.zeroNode.label == "Zero":
            zero += " 0"
            print(zero)
        elif self.leadingNode.leafOne and self.leadingNode.zeroNode.label == "One":
            zero += " 1"
            print(zero)
        else:
            print(zero)
            self.printTreeHelper(pipelines, self.leadingNode.zeroNode)
        one = self.leadingNode.label + " = 1 :"
        if self.leadingNode.leafZero and self.leadingNode.oneNode.label == "Zero":
            one += " 0"
            print(one)
        elif self.leadingNode.leafOne and self.leadingNode.oneNode.label == "One":
            one += " 1"
            print(one)
        else:
            print(one)
            self.printTreeHelper(pipelines, self.leadingNode.oneNode)

    def printTreeHelper(self, pipelines, n):
        pipelines += 1
        zero = ""
        one = ""
        for i in range(pipelines):
            zero += "| "
            one += "| "
        zero += n.label + " = 0 :"
        try:
            if n.leafZero:
                zero += " 0"
                print(zero)
            elif n.leafOne:
                zero += " 1"
                print(zero)
            else:
                print(zero)
                self.printTreeHelper(pipelines, n.zeroNode)
        except:
            0
        try:
            one += n.label + " = 1 :"
            if n.leafZero:
                one += " 0"
                print(one)
            elif n.leafOne:
                one += " 1"
                print(one)
            if not n.leafZero or not n.leafOne:
                #print(one)
                self.printTreeHelper(pipelines, n.oneNode)
        except:
            1

    def test(self, testingFileName):
        correct = 0
        total = 0
        tf = pd.read_csv(testingFileName)
        classCol = tf[['Class']]
        for i, row in tf.iterrows():
            answer = -1
            if row[self.leadingNode.label] == 0:
                if self.leadingNode.leafZero:
                    answer = 0
                else:
                    answer = self.testHelper(self.leadingNode.zeroNode, row)
            elif row[self.leadingNode.label] == 1:
                if self.leadingNode.leafOne:
                    answer = 1
                else:
                    answer = self.testHelper(self.leadingNode.oneNode, row)
            classAnswer = int(classCol.values[i])
            total += 1
            if(answer == classAnswer):
                correct += 1
        return correct/total

    def testHelper(self, n, row): #todo finish
        if row[n.label] == 0:
            if n.leafZero:
                return 0
            else:
                return self.testHelper(n.zeroNode, row)
        elif row[n.label] == 1:
            if n.leafOne:
                return 1
            else:
                return self.testHelper(n.oneNode, row)

def postPruning(dt, l, k, valSet):
    dBest = dt
    tBest = dBest.test(valSet)
    for i in range(l):
        dPrime = dt
        m = rd.randint(1, k)
        for j in range(m):
            n = 0 #todo n equals number of nonleaf nodes
            #todo order nodes for 1 to n
            p = rd.randint(1, n)
            #todo make node p a leaf based on the majority of data
        tPrime = dPrime.test(valSet)
        if tPrime > tBest:
            dBest = dPrime
    return dBest #todo should return the percentage along with the tree



def entropy(matches, mismatches):
    total = matches + mismatches
    if total == 0:
        return 0#float('nan')
    first = -1 * (matches / total) * np.log2(matches / total)
    second = -1 * (mismatches / total) * np.log2(mismatches / total)
    return first + second


def varianceImpurity(zeroes, ones):
    total = ones + zeroes
    if total == 0:
        return 0#float('nan')
    first = ones / total
    second = zeroes / total
    return first * second


class node:
    zeroNode = None
    oneNode = None
    label = None
    leafZero = False
    leafOne = False
    zeroAnswer = -1
    oneAnswer = -1
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
        if self.total == 0:
            return 0#float('nan')
        first = entropy(self.matchesOne+self.mismatchesZero, self.matchesZero+self.mismatchesOne)
        second = ((self.matchesOne+self.mismatchesOne)/self.total) * entropy(self.matchesOne, self.mismatchesOne)
        third = ((self.matchesZero+self.mismatchesZero)/self.total) * entropy(self.mismatchesZero, self.matchesZero)
        return first - second - third

    def gainVI(self):
        if self.total == 0:
            return 0#float('nan')
        first = varianceImpurity(self.matchesOne + self.mismatchesZero, self.matchesZero + self.mismatchesOne)
        second = ((self.matchesOne+self.mismatchesOne)/self.total) * varianceImpurity(self.matchesOne, self.mismatchesOne)
        third = ((self.matchesZero + self.mismatchesZero) / self.total) * varianceImpurity(self.mismatchesZero, self.matchesZero)
        return first - second - third


def buildTree(trainingFileName, vOrE):
    global illegal
    illegal = ["Class"]
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
                    #print(n.gain())
                    best = n
                if best.gain() < n.gain():
                    #print(n.gain())
                    best = n
            else:
                if best.label == "":
                    #print(n.gainVI())
                    best = n
                if best.gain() < n.gain():
                    #print(n.gainVI())
                    best = n
    illegal.append(best.label)
    print(illegal)
    print("root " + best.label)
    best, best.oneNode = buildTreeHelper(trainingFileName, vOrE, best, 1)
    try:
        print("on of " + best.label + " is " + best.oneNode.label)
    except:
        0
    best, best.zeroNode = buildTreeHelper(trainingFileName, vOrE, best, 0)
    try:
        print("zn of " + best.label + " is " + best.zeroNode.label)
    except:
        0



    dt = decisionTree()
    dt.addNode(best)
    return dt


def buildTreeHelper(trainingFileName, vOrE, parent, zOrO):
    global illegal
    best = node("best")
    n = node("")
    tf = pd.read_csv(trainingFileName)
    classCol = tf[['Class']]
    parentDF = tf[[parent.label]]
    for key, value in tf.iteritems():
        # print(key)
        # print(illegal)
        if key not in illegal:
            print(key)
            i = 0
            n = node(key)
            for element in value:
                element = int(element)
                answer = int(classCol.values[i])
                parentVal = int(parentDF.values[i])
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
                    #print(n.gain())
                    best = n
                if best.gain() < n.gain():
                    #print(n.gain())
                    best = n
            else:
                if best.label == "":
                    #print(n.gainVI())
                    best = n
                if best.gain() < n.gain():
                    #print(n.gainVI())
                    best = n
    if best.label == "best":
        if zOrO == 1:
            parent.leafOne = True
            if parent.matchesOne > parent.mismatchesOne:
                child = node("One")
            else:
                child = node("Zero")
        else:
            parent.leafZero = True
            if parent.matchesZero > parent.mismatchesZero:
                child = node("Zero")
            else:
                child = node("One")
        return parent, child

    modified = False
    if np.isnan(entropy(best.matchesOne, best.mismatchesOne)):#entropy(best.matchesOne, best.mismatchesOne) == 0:
        best.leafOne = True
        if best.matchesOne > best.mismatchesOne:
            best.oneNode = node("One")
        else:
            best.oneNode = node("Zero")
        modified = True
    if np.isnan(entropy(best.matchesZero, best.mismatchesZero)):#entropy(best.matchesZero, best.mismatchesZero) == 0:
        best.leafZero = True
        if best.matchesZero > best.mismatchesZero:
            best.zeroNode = node("Zero")
        else:
            best.zeroNode = node("One")
        modified = True
    if modified:
        print("return modified")
        return parent, best

    illegal.append(best.label)
    print(illegal)
    if len(illegal) >= 20:
        if best.matchesZero > best.matchesOne:
            best.oneNode = node("Zero")
            best.leafZero = True
        else:
            best.oneNode = node("One")
            best.leafOne = True
        print("return illegal")
        return parent, best

    best, best.oneNode = buildTreeHelper(trainingFileName, vOrE, best, 1)
    try:
        print("on of " + best.label + " is " + best.oneNode.label)
    except:
        0
    best, best.zeroNode = buildTreeHelper(trainingFileName, vOrE, best, 0)
    try:
        print("zn of " + best.label + " is " + best.zeroNode.label)
    except:
        0
    print("return end")
    return parent, best
#todo figure out when something should be a leaf
#todo implement pruning
