import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import time
import matplotlib.animation as anim
from matplotlib.animation import FuncAnimation
import matplotlib
matplotlib.use('TkAgg')
def showImageVSPrediction(imagePaths, reconstruction_cost):
    updatedLoss = []
    f, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
    def animate(inp):
        imagePath, cost = inp
        updatedLoss.append(cost)

        plt.cla()
        image = mpimg.imread(imagePath)
        ax1.imshow(image)
        ax1.set_title('Test Video')
        
        ax2.plot(range(len(updatedLoss)), updatedLoss, label="ReconstructionCost")
        ax2.legend(loc='best')
        ax2.grid()
        ax2.set_xlabel('sample index')
        ax2.set_ylabel('loss')
        plt.tight_layout()
        


        
        # plt.cla()
        # plt.plot(range(len(updatedLoss)), updatedLoss, linestyle='-', linewidth=1, label="ReconstructionCost")
        # plt.legend(loc='best')
        # plt.grid()
        # plt.xlabel('sample index')
        # plt.ylabel('loss')
        # plt.tight_layout()
    ani = FuncAnimation(plt.gcf(), animate, frames = zip(imagePaths, reconstruction_cost), repeat = False, interval=10)
    plt.tight_layout()
    plt.show()

def showImage(path):
    img = mpimg.imread(path)
    imgplot = plt.imshow(img)
    plt.show()
def s2howImageVSPrediction(imgPath, reconstruction_cost):
    f, (ax1, ax2) = plt.subplots(1, 2, sharey=True)
    image = mpimg.imread(imgPath)
    ax1.imshow(image)
    ax1.set_title('Test Video')
    
    ax2.plot(range(len(reconstruction_cost)), reconstruction_cost, linestyle='-', linewidth=1, label="ReconstructionCost")
    ax2.legend(loc='best')
    ax2.grid()
    ax2.set_xlabel('sample index')
    ax2.set_ylabel('loss')

    plt.show()

    plt.draw()
    plt.pause(0.1)
    plt.clf()
    # ax2.clf()