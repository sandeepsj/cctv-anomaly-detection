import getDataSet
import Config
import getModel
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from numpy.core.fromnumeric import mean, shape
import pickle
from target import TARGET
import display

model_name = Config.MODEL_NAME

def evaluate():
    x_train = getDataSet.get_dataset()
    print("dataset shape : ", shape(x_train))
    print("data loaded ....................................100%")
    model = getModel.get_model(x_train)
    print("model loaded ....................................100%")
    x_test = getDataSet.get_testset()
    print("testset loaded ....................................100%")

    # plot
    def plotLoss(reconstruction_cost, path=Config.RESULT_PATH):
        plt.plot(range(len(reconstruction_cost)), reconstruction_cost, linestyle='-', linewidth=1, label=model_name)
        plt.legend(loc='best')
        plt.grid()
        plt.xlabel('sample index')
        plt.ylabel('loss')
        plt.savefig(path)
        plt.clf()

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
    if Config.TESTSET_STRUCTURE == "dict":
        result = {}
        print("testset shape : ", shape(x_test))
        for dir in x_test:
            print("computing anomaly score and plotting for >>> " + dir)
            # compule loss for each test sample
            cur_test = np.array(x_test[dir])
            cur_test = cur_test.reshape(-1, 128,128,1)
            losses = []
            frameCount = 1
            imagePaths = []
            for x in cur_test:
                x = np.expand_dims(x, axis=0)
                loss = model.test_on_batch(x, x)
                losses.append(loss)
                # display frame and loss and wait for 0.1 sec
                imagePaths.append(Config.TESTSET_PATH + "/"+dir+"/"+getFileName(frameCount))
                frameCount += 1
            display.showImageVSPrediction(imagePaths, losses)
            result[dir] = losses
            plotLoss(losses, Config.RESULT_PATH + "/" + dir)
        resFile = open(Config.RESULT_PATH+"/result", 'wb')
        print("about to dumb results")
        pickle.dump(result, resFile)
        print("Results dumped to result")
        resFile.close()
        getAccuracy()
    else:
        print("testset shape : ", shape(x_test))

        x_test = x_test.reshape(-1,128,128,1)
        x_concat = np.concatenate([x_test], axis=0)
        losses = []
        for x in x_concat:
            # compule loss for each test sample
            x = np.expand_dims(x, axis=0)
            loss = model.test_on_batch(x, x)
            losses.append(loss)
        plotLoss(losses)


def validate(frameRCost, t):
        for (start, end) in t:
            if frameRCost>=start and frameRCost<=end:
                return True
        return False

def getSingleTestAccuracy(testName, result, target):
    cur_TP = 0
    cur_FN = 0
    cur_TOTAL = 0
    if (testName[-3:] == "_gt"):
        return -1
    threshold = mean(result) * 1.1
    print("threshold of ", testName, " >>> ", threshold)
    for cost in result:
        if cost >= threshold:
            if validate(cost, target):
                cur_TP += 1
        else:
            if not validate(cost, target):
                cur_FN += 1
        cur_TOTAL += 1
    cur_accuracy = (cur_FN+cur_TP)/(cur_TOTAL)
    print("accuracy for "+ testName + " >>> ", cur_accuracy )
    return cur_accuracy

def getAccuracy():
    resFile = open(Config.RESULT_PATH+"/result", "rb")
    results = pickle.load(resFile)
    resFile.close()
    # target = open(Config.TARGET_PATH, "rb") need to add .m file support\
    
    cnt = 0
    TP = 0
    FN = 0
    TOTAL = 0
    for test in results:
        cur_TP = 0
        cur_FN = 0
        cur_TOTAL = 0
        target = TARGET[cnt]
        result = results[test]
        if (test[-3:] == "_gt"):
            continue
        threshold = mean(result) * 1.1
        print("threshold of ", test, " >>> ", threshold)
        for cost in result:
            if cost >= threshold:
                if validate(cost, target):
                    TP += 1
                    cur_TP += 1
            else:
                if not validate(cost, target):
                    FN += 1
                    cur_FN += 1
            TOTAL += 1
            cur_TOTAL += 1
        cnt += 1
        cur_accuracy = (cur_FN+cur_TP)/(cur_TOTAL)
        print("accuracy for "+ test + " >>> ", cur_accuracy )
    accuracy = (TP + FN)/(TOTAL)
    print("Overall Accuracy of the model >>> ", accuracy)
    return accuracy
    
if Config.LOAD_RESULT_FROM_CACHE:
    getAccuracy()
else:
    evaluate()

# temp = getDataSet.get_dataset()
# print("loaded dataset")
# keys = list(temp.keys())
# print("number of keys: ", len(keys))
# folder = keys[0]
# print("folder: ", folder)
# firstFolder = temp[folder]
# print("number of elements in first level: ", len(firstFolder))
# firstImageOpticalFlow = firstFolder[0]
# print("first optical flow: ", firstImageOpticalFlow)
# firstRow = firstImage[0]
# print("len(firstRow) : ", len(firstRow))
# firstCell = firstRow[0]
# print("len(firstCell) : ", len(firstCell))
# firstCellMag = firstCell["mag"]
# print("firstCellMag : ", firstCellMag)
# firstCellAng = firstCell["ang"]
# print("firstCellAng : ", firstCellAng)

# print(len(temp[0][0]))
# print(len(temp[0][0][0]))