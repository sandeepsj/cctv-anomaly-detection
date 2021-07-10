
import pickle

import numpy as np
from numpy.core.fromnumeric import mean, shape

import Config
import display
import getDataSet
import getModel
from target import TARGET


def getModelAccuracy(model):
    evaluate(model)
    return getBestThreshold()

def evaluate(model):
    print("model loaded ....................................100%")
    x_test = getDataSet.get_testset()
    print("testset loaded ....................................100%")
    def getFileName(frameCount):
        filename = "000.tif" 
        cntstr = str(frameCount)
        if len(cntstr) == 1:
            filename = "00"+cntstr+".tif"
        elif len(cntstr) == 2:
            filename = "0"+cntstr+".tif"
        else:
            filename = cntstr+".tif"
        return filename
    # test

    result = {}
    
    paddingIndex = {}
    print("testset shape : ", shape(x_test))
    for dir in x_test:
        # compule loss for each test sample
        cur_test = np.array(x_test[dir])
        cur_test = cur_test.reshape(-1, Config.IMAGE_SHAPE_X,Config.IMAGE_SHAPE_Y,1)
        losses = []
        frameCount = 1
        imagePaths = []
        padding = float('inf')
        for x in cur_test:
            x = np.expand_dims(x, axis=0)
            #loss = model.test_on_batch(x, x)
            trainPredict = model.predict(x)
            loss = np.sum(np.abs(trainPredict - x))
            padding = min(padding, loss)
            losses.append(loss)
            # display frame and loss and wait for 0.1 sec
            imagePaths.append(Config.TESTSET_PATH + "/"+dir+"/"+getFileName(frameCount))
            frameCount += 1
        for i in range(len(losses)):
            losses[i] = losses[i] - padding
        paddingIndex[dir] = padding
        
        result[dir] = losses
    resFile = open(Config.RESULT_PATH+"/result", 'wb')
    print("about to dumb results")
    pickle.dump(result, resFile)
    print("Results dumped to result")
    resFile.close()
    

def validate(frameRCost, t):
    for (start, end) in t:
        if frameRCost>=start and frameRCost<=end:
            return True
    return False


def getAccuracy(showLogs = True, threshold = None):
    resFile = open(Config.RESULT_PATH+"/result", "rb")
    results = pickle.load(resFile)
    resFile.close()
    # target = open(Config.TARGET_PATH, "rb") need to add .m file support\
    
    cnt = 0
    TP = 0
    FN = 0
    TOTAL = 0
    bestCases = []
    
    for test in results:
        cur_TP = 0
        cur_FN = 0
        cur_TOTAL = 0
        target = TARGET[cnt]
        result = results[test]
        if (test[-3:] == "_gt"):
            continue
        if threshold == None:
            threshold = Config.THRESHOLD_VALUE * Config.THRESHOLD_SCALING_FACTOR
        if threshold == None:
            threshold = mean(result) * Config.THRESHOLD_SCALING_FACTOR
        # threshold=480
        if showLogs:
            print("threshold of ", test, " >>> ", threshold)
        frameCount = 1
        Sum = threshold
        for cost in result:
            #threshold = (Sum + cost)/frameCount\
            
            if cost >= threshold:
                if validate(frameCount, target):
                    TP += 1
                    cur_TP += 1
            else:
                if not validate(frameCount, target):
                    FN += 1
                    cur_FN += 1
            
            TOTAL += 1
            cur_TOTAL += 1
            frameCount += 1
        if showLogs:
            print(cur_TP, cur_FN)
        cnt += 1
        cur_accuracy = (cur_FN+cur_TP)/(cur_TOTAL)
        if cur_accuracy>=0.80:
            bestCases.append(test)
        if showLogs:
            print("accuracy for "+ test + " >>> ", cur_accuracy )
    accuracy = (TP + FN)/(TOTAL)
    if showLogs:
        print("Overall Accuracy of the model >>> ", accuracy)
    return accuracy, bestCases

def getBestThreshold():
    bestAcc = 0
    bestThresh = 0
    
    bestToShow = {"threshold":0, "bestCases": 0, "cases":[]}
    print("finding best threshold")
    for i in range(0, 400):
        
        curAcc, bestCases = getAccuracy(False, i)
        if bestToShow["bestCases"]<len(bestCases):
            bestToShow = {"threshold":i, "bestCases":len(bestCases), "cases":tuple(bestCases)}
        if bestAcc < curAcc:
            print("New Best ***")
            print("accuracy: ", curAcc, "Threshold: ", bestThresh)
            bestAcc = curAcc
            bestThresh = i
        #print("accuracy for", i, curAcc)
    print(bestToShow)
    print("Threshold of:", bestThresh, "gives accuracy of", bestAcc, "\n thats the best of this model");
    return bestAcc
