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
            for x in cur_test:
                x = np.expand_dims(x, axis=0)
                loss = model.test_on_batch(x, x)
                losses.append(loss)
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

def getAccuracy():
    resFile = open(Config.RESULT_PATH+"/result", "rb")
    results = pickle.load(resFile)
    resFile.close()
    # target = open(Config.TARGET_PATH, "rb") need to add .m file support\
    def validate(frame, t):
        for (start, end) in t:
            if frame>=start and frame<=end:
                return True
        return False
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
                if validate(cnt, target):
                    TP += 1
                    cur_TP += 1
            else:
                if not validate(cnt, target):
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