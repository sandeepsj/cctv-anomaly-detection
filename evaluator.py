import matplotlib
import numpy as np

import Config
import getDataSet
import getModel

matplotlib.use('Agg')
import pickle

import matplotlib.pyplot as plt
from numpy.core.fromnumeric import mean, shape

import display
from target import TARGET

model_name = Config.MODEL_NAME

def getSingleFrameCost(model, fileName, single_test_case_name, test_set_path):
    cur_test = getDataSet.get_single_frame(fileName, single_test_case_name, test_set_path)
    cur_test = cur_test.reshape(Config.IMAGE_SHAPE_X,Config.IMAGE_SHAPE_Y,1)
    x = cur_test
    x = np.expand_dims(x, axis=0)
    loss = model.test_on_batch(x, x)
    return loss

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
    if Config.TESTSET_STRUCTURE == "dict" and not Config.CALCULATE_THRESHOLD:
        result = {}
        print("testset shape : ", shape(x_test))
        for dir in x_test:
            if Config.USE_SINGLE_TEST_CASE and dir != Config.SINGLE_TEST_CASE_NAME:
                continue
            print("computing anomaly score and plotting for >>> " + dir)
            # compule loss for each test sample
            cur_test = np.array(x_test[dir])
            cur_test = cur_test.reshape(-1, Config.IMAGE_SHAPE_X,Config.IMAGE_SHAPE_Y,1)
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
            if (Config.DISPAY_OUTPUT):
                display.showImageVSPrediction(imagePaths, losses)
            result[dir] = losses
            plotLoss(losses, Config.RESULT_PATH + "/" + dir)
        resFile = open(Config.RESULT_PATH+"/result", 'wb')
        print("about to dumb results")
        pickle.dump(result, resFile)
        print("Results dumped to result")
        resFile.close()
        getAccuracy()
    elif not Config.CALCULATE_THRESHOLD:
        print("testset shape : ", shape(x_test))

        x_test = x_test.reshape(-1,Config.IMAGE_SHAPE_X,Config.IMAGE_SHAPE_Y,1)
        x_concat = np.concatenate([x_test], axis=0)
        losses = []
        for x in x_concat:
            # compule loss for each test sample
            x = np.expand_dims(x, axis=0)
            loss = model.test_on_batch(x, x)
            losses.append(loss)
        plotLoss(losses)
    else:
        print("testset shape : ", shape(x_test))

        x_test = x_test.reshape(-1,Config.IMAGE_SHAPE_X,Config.IMAGE_SHAPE_Y,1)
        x_concat = np.concatenate([x_test], axis=0)
        losses = []
        i = 0
        for x in x_concat:
            if i%200 == 0:
                print("done", i//200)
            i += 1

            # compule loss for each test sample
            x = np.expand_dims(x, axis=0)
            loss = model.test_on_batch(x, x)
            losses.append(loss)
        threshold = mean(losses)
        print("Threshold value is >>> ", threshold)
        print("Padded Threshold value is >>> ", threshold*Config.THRESHOLD_SCALING_FACTOR)


def validate(frameRCost, t):
    for (start, end) in t:
        if frameRCost>=start and frameRCost<=end:
            return True
    return False


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
        threshold = Config.THRESHOLD_VALUE * Config.THRESHOLD_SCALING_FACTOR
        if threshold == None:
            threshold = mean(result) * Config.THRESHOLD_SCALING_FACTOR
        print("threshold of ", test, " >>> ", threshold)
        frameCount = 1
        for cost in result:
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
        print(cur_TP, cur_FN)
        cnt += 1
        cur_accuracy = (cur_FN+cur_TP)/(cur_TOTAL)
        print("accuracy for "+ test + " >>> ", cur_accuracy )
    accuracy = (TP + FN)/(TOTAL)
    print("Overall Accuracy of the model >>> ", accuracy)
    return accuracy

if __name__ == "__main__":
    if Config.LOAD_RESULT_FROM_CACHE:
        getAccuracy()
    else:
        evaluate()


# def getSingleTestAccuracy(testName, result, target):
#     cur_TP = 0
#     cur_FN = 0
#     cur_TOTAL = 0
#     if (testName[-3:] == "_gt"):
#         return -1
#     threshold = Config.THRESHOLD_VALUE * Config.THRESHOLD_SCALING_FACTOR
#     if threshold == None:
#         threshold = mean(result) * Config.THRESHOLD_SCALING_FACTOR
    
#     print("threshold of ", testName, " >>> ", threshold)
#     for cost in result:
#         if cost >= threshold:
#             if validate(cost, target):
#                 cur_TP += 1
#         else:
#             if not validate(cost, target):
#                 cur_FN += 1
#         cur_TOTAL += 1
#     cur_accuracy = (cur_FN+cur_TP)/(cur_TOTAL)
#     print("accuracy for "+ testName + " >>> ", cur_accuracy )
#     return cur_accuracy

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
