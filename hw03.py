import sys, copy, math

testDict = dict()
uniformDict = dict()
unigramDict = dict()
bigramDict = dict()
trigramDict = dict()
unknowntok = "UNKNOWNWORD"
startChar = "STARTCHAR"
stopChar = "STOPCHAR"
vocabLen = 0
totalLen = 0

INCLUDEPUNCTUATION = True
VERBOSE = False
MAX_NUMBER_TO_PRINT = 200

def printTuple(t):
    buf = ""
    for i in xrange(len(t)):
        if i == 0:
            buf += str(t[len(t) - 1]) + "|"
        elif i == len(t) - 1:
            buf += str(t[0])
        else:
            buf += str(t[len(t) - 1 - i]) + ", "
    return buf

def prettyPrint(L):
    for item in L:
        print ("p(" + printTuple(item[0]) + ") = %f" % item[1])

def uniform():
    print "Constructing uniform dict...",
    sys.stdout.flush()
    uniDict = { k : 1.0/vocabLen for k in unigramDict}
    print "Done!"
    return uniDict

def unigram():
    print "Constructing unigram dict...",
    sys.stdout.flush()
    uniDict = { k : float(unigramDict[k])/totalLen for k in unigramDict}
    print "Done!"
    return uniDict

def bigram(trainL):
    trainList = copy.deepcopy(trainL)
    print "Running Bigram model:"

    print "    Constructing bigram list...",
    sys.stdout.flush()
    biList = []
    trainList.insert(0,startChar)
    for i in xrange(len(trainList)-1):
        biList.append( (trainList[i], trainList[i+1]) )
    biList.sort()
    print "Done!"

    print "    Adding entries to bigram dict...",
    sys.stdout.flush()
    curFirstWord = biList[0][0]
    curSecondWord = biList[0][1]
    tempList = []
    firstWordCtr = 0
    secondWordCtr = 0
    for item in biList:
        if item[0] == curFirstWord:
            firstWordCtr += 1
            if item[1] == curSecondWord:
                secondWordCtr += 1
            else:
                tempList.append( ((curFirstWord,
                                   curSecondWord), secondWordCtr) )
                curSecondWord = item[1]
                secondWordCtr = 1
        else:
            # capture the last word.
            bigramDict[(curFirstWord,
                        curSecondWord)] = float(secondWordCtr)/firstWordCtr
            for pair in tempList:
                bigramDict[pair[0]] = float(pair[1])/firstWordCtr
            curFirstWord = item[0]
            curSecondWord = item[1]
            tempList = []
            firstWordCtr = 1
            secondWordCtr = 1
            
    #Add the final result to the dict:
    bigramDict[(curFirstWord,
                curSecondWord)] = float(secondWordCtr)/firstWordCtr
    print "Done!"
    print ("    Number of bigrams: %d" % len(bigramDict))
    return bigramDict

def trigram(trainL):
    trainList = copy.deepcopy(trainL)
    print "Running Trigram model:"

    print "    Constructing trigram list...",
    sys.stdout.flush()
    triList = []
    trainList.insert(0,startChar)
    trainList.insert(0,startChar)
    for i in xrange(len(trainList)-2):
        triList.append( (trainList[i], trainList[i+1], trainList[i+2]) )
    triList.sort()
    print "Done!"
    
    print "    Adding entries to trigram dict...",
    sys.stdout.flush()
    curFirstWord = triList[0][0]
    curSecondWord = triList[0][1]
    curThirdWord = triList[0][2]
    tempList = []
    secondWordCtr = 0
    thirdWordCtr = 0
    for item in triList:
        if item[0] == curFirstWord:
            if item[1] == curSecondWord:
                secondWordCtr += 1
                if item[2] == curThirdWord:
                    thirdWordCtr += 1
                else:
                    tempList.append( ((curFirstWord,
                                        curSecondWord,
                                        curThirdWord), thirdWordCtr) )
                    curThirdWord = item[2]
                    thirdWordCtr = 1
            else:
                trigramDict[(curFirstWord,
                             curSecondWord,
                             curThirdWord)] = float(thirdWordCtr)/secondWordCtr
                for triple in tempList:
                    trigramDict[triple[0]] = float(triple[1])/secondWordCtr
                curSecondWord = item[1]
                curThirdWord = item[2]
                tempList = []
                secondWordCtr = 1
                thirdWordCtr = 1
        else:
            trigramDict[(curFirstWord,
                        curSecondWord,
                        curThirdWord)] = float(thirdWordCtr)/secondWordCtr
            curFirstWord = item[0]
            curSecondWord = item[1]
            curThirdWord = item[2]
            tempList = []
            secondWordCtr = 1
            thirdWordCtr = 1
            
    #Add the final result to the dict:
    trigramDict[(curFirstWord,
                curSecondWord,
                curThirdWord)] = float(thirdWordCtr)/secondWordCtr
    print "Done!"
    print ("    Number of trigram: %d" % len(trigramDict))
    return trigramDict


def driver(lamb0, lamb1, lamb2, lamb3, testFile, trainFiles):
    global vocabLen, totalLen
    global uniformDict, unigramDict
    global bigramDict, trigramDict
    #print lamb0, lamb1, lamb2, lamb3, testFile, trainFile
    (lamb0, lamb1, lamb2, lamb3) = (float(lamb0), float(lamb1),
                                    float(lamb2), float(lamb3))
    testbuf = ""
    trainbuf = ""
    fileStr = ""
    
    testVar = 13.37
    if ((lamb0 + lamb1 + lamb2 + lamb3) * testVar != testVar):
        print "Error: Lambda values must sum to 1.0!"
        return
    
    print "Begin Model Training (Powered by Eric Gan)..."
    
    print "Opening Training File...",
    sys.stdout.flush()
    for trainFile in trainFiles: 
        trainfd = open(trainFile, "r")
        fileStr = trainfd.readline()
        while (fileStr != ""):
            trainbuf += fileStr
            fileStr = trainfd.readline()
        trainfd.close()
    print "Done!"
    
    print "Creating training text token list...",
    sys.stdout.flush()
    trainbuf = trainbuf.lower()
    trainList = "".join(trainbuf.split("\n")).split(" ")
    if len(trainList) == 0: return
    
    # Comment out this line if we want to include punctuation in our vocab.
    if not INCLUDEPUNCTUATION: 
        trainList = filter(str.isalnum, trainList)
    
    sortedTrainList = copy.deepcopy(trainList)
    sortedTrainList.sort()
    print "Done!"
    
    print "Creating counting dictionary...",
    sys.stdout.flush()
    unigramDict[unknowntok] = 0
    curElem = sortedTrainList[0]
    for item in sortedTrainList:
        if item != curElem: curElem = item
        if curElem not in unigramDict:
            unigramDict[curElem] = 0
        unigramDict[curElem] += 1
    print "Done!"
    
    # To avoid conflict with destructive deletion of keys, we create a buffer
    # of keys to be deleted later (namely after we exit the loop).
    print "Replacing all infrequent words with UNKNOWNWORD token...",
    sys.stdout.flush()
    toDelete = []
    for key in unigramDict:
        if unigramDict[key] < 5:
            unigramDict[unknowntok] += unigramDict[key]
            toDelete.append(key)
    for key in toDelete:
        del unigramDict[key]
        
    trainList = map(lambda x: unknowntok if x in toDelete else x, trainList)
    print "Done!"
    
    vocabLen = len(unigramDict)
    totalLen = len(trainList)
    
    print "----------------------------------------"
    print ("    Vocabulary size: %d" % vocabLen)
    print ("    Total words: %d" % totalLen)
    print "----------------------------------------"
    
    print "Begin constructing probability models:"
    uniformDict = uniform()
    unigramDict = unigram()
    bigramDict = bigram(trainList)
    trigramDict = trigram(trainList)
    
    unigramList = [(k,unigramDict[k]) for k in unigramDict]
    unigramList.sort(key=lambda x: x[1])
    
    if VERBOSE:
        print "VERBOSE is on: Printing most common n-grams..."
        print "----------------------------------------"
        print "Some of the most common unigrams (top 30): "
        for i in xrange(30):
            print unigramList[len(unigramList)-1-i]
        print "----------------------------------------"
        print
        print 
        bigramList = [(k,bigramDict[k]) for k in bigramDict]
        bigramList.sort(key=lambda x: x[1])
        mostCommonBigrams = filter(lambda x: x[1] > 0.85, bigramList)
        print "----------------------------------------"
        print "Some of the most common bigrams (p > 0.85): "
        if len(mostCommonBigrams) <= MAX_NUMBER_TO_PRINT:
            prettyPrint(mostCommonBigrams)
        else:
            print "List too large! Skipping..."
        print "----------------------------------------"
        print
        print 
        trigramList = [(k,trigramDict[k]) for k in trigramDict]
        trigramList.sort(key=lambda x: x[1])
        mostCommonTrigrams = filter(lambda x: x[1] > 0.85, trigramList)
        print "----------------------------------------"
        print "Some of the most common trigrams (p > 0.85): "
        if len(mostCommonTrigrams) <= MAX_NUMBER_TO_PRINT:
            prettyPrint(mostCommonTrigrams)
        else:
            print "List too large! Skipping..."
        print "----------------------------------------"

    print "Training Complete!"
    raw_input("Press enter to continue to testing ---->")
    
    print "Opening test file...",
    sys.stdout.flush()
    if testFile != "0":
        testfd = open(testFile, "r")
        fileStr = testfd.readline()
        while (fileStr != ""):
            testbuf += fileStr
            fileStr = testfd.readline()
        testfd.close()
    print "Done!"
    
    print "Creating testing text token list...",
    sys.stdout.flush()
    testbuf = testbuf.lower()
    testList = "".join(testbuf.split("\n")).split(" ")
    if len(testList) == 0: return
    
    # Comment out this line if we want to include punctuation in our vocab.
    if not INCLUDEPUNCTUATION: 
        testList = filter(str.isalnum, testList)
    
    sortedTestList = copy.deepcopy(testList)
    sortedTestList.sort()
    print "Done!"
    
    print "Creating counting dictionary...",
    sys.stdout.flush()
    testDict[unknowntok] = 0
    curElem = sortedTestList[0]
    for item in sortedTestList:
        if item != curElem: curElem = item
        if curElem not in testDict:
            testDict[curElem] = 0
        testDict[curElem] += 1
    print "Done!"    

    print "Replacing all infrequent words with UNKNOWNWORD token...",
    sys.stdout.flush()
    toDelete = []
    for key in testDict:
        if testDict[key] < 5:
            testDict[unknowntok] += testDict[key]
            toDelete.append(key)
    for key in toDelete:
        del testDict[key]
        
    testList = map(lambda x: unknowntok if x in toDelete else x, testList)
    print "Done!"
    
    print "Replacing words not in vocabulary with UNKNOWNWORD token...",
    sys.stdout.flush()
    for i in xrange(len(testList)):
        if testList[i] not in unigramDict:
            testList[i] = unknowntok
    print "Done!"

    uniList = []
    biList = []
    triList = []

    print "Creating Unigram List...",
    sys.stdout.flush()
    uniList = copy.deepcopy(testList)
    print "Done!"
    
    print "Creating Bigram List...",
    sys.stdout.flush()
    testListCopy = copy.deepcopy(testList)
    testListCopy.insert(0,startChar)
    for i in xrange(len(testListCopy)-1):
        biList.append( (testListCopy[i], testListCopy[i+1]) )
    print "Done!"
    
    print "Creating Trigram List...",
    sys.stdout.flush()
    testListCopy = copy.deepcopy(testList)
    testListCopy.insert(0,startChar)
    testListCopy.insert(0,startChar)
    for i in xrange(len(testListCopy)-2):
        triList.append( (testListCopy[i],
                         testListCopy[i+1],
                         testListCopy[i+2]) )
    print "Done!"
    
    unifLen = len(testList)
    uniLen = len(uniList)
    biLen = len(biList)
    triLen = len(triList)
    
    print "----------------------------------------"
    print ("    Vocab size: %d" % unifLen)
    print ("    Unigram size: %d" % uniLen)
    print ("    Bigram size: %d" % biLen)
    print ("    Triigram size: %d" % triLen)
    print "----------------------------------------"
    
    print "Begin Perplexity Calculation (Linear Interpolation)"
    print ("    lambda values: %02f %02f %02f %02f"
           % (lamb0, lamb1, lamb2, lamb3))
    
    runningSum = 0.0
    unifProb = 0.0
    uniProb = 0.0
    biProb = 0.0
    triProb = 0.0
    pow10 = 0
    for i in xrange(unifLen):
        if testList[i] in uniformDict:
            unifProb = uniformDict[testList[i]]
        if uniList[i] in unigramDict:
            uniProb = unigramDict[uniList[i]]
        if biList[i] in bigramDict:
            biProb = bigramDict[biList[i]]
        if triList[i] in trigramDict:
            triProb = trigramDict[triList[i]]
            
        # We need to do an unfortunate small hack to handle the case where
        # the weight is 0. This will add more variability to our data set.
        # TODO: Find a way to better deal with this problem.
        weightedValue = (lamb0*unifProb + lamb1*uniProb
                        + lamb2*biProb + lamb3*triProb)
        if weightedValue == 0.0: continue
        runningSum += math.log(weightedValue)
        unifProb = 0.0
        uniProb = 0.0
        biProb = 0.0
        triProb = 0.0
        pow10 += 1
    perplexity = math.exp(-runningSum / unifLen)
    print "Done! Perplexity =", perplexity

if __name__ == "__main__":
    if len(sys.argv) < 7:
        print "Usage:",
        print ("python %s [lamb0] [lamb1] [lamb2]" % sys.argv[0]),
        print "[lamb3] [testfile] [trainingfile(s)]"
        exit(0)
    driver(sys.argv[1], sys.argv[2], sys.argv[3],
           sys.argv[4], sys.argv[5], sys.argv[6:])
