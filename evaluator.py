import getDataSet
import Config
import getModel
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from numpy.core.fromnumeric import shape

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
            plotLoss(losses, Config.RESULT_PATH + "/" + dir)
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