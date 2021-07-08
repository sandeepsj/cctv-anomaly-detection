import shelve
from os import listdir
from os.path import isdir, join

import cv2
import numpy as np

import Config
import processor


def get_dataset(re=Config.RELOAD_DATASET):
    cache = shelve.open(Config.CACHE_PATH + "dataset")
    if not re:
          return  np.array(cache["dataset"])
    sz = 20
    opticalFlowClips = {}
    clips = []
    cnt = 0
    container = np.zeros(shape=(256, 256, 10))
    for f in sorted(listdir(Config.DATASET_PATH)):
        if isdir(join(Config.DATASET_PATH, f)):
            print(f)
            all_frames = []
            cnt = 0
            cur_gray = None
            if Config.USE_OPTICAL_FLOW:
                for c in sorted(listdir(join(Config.DATASET_PATH, f))):
                    if str(join(join(Config.DATASET_PATH, f), c))[-3:] == "tif":
                        old_gray = cur_gray
                        cur_gray = cv2.imread(join(join(Config.DATASET_PATH, f), c), cv2.COLOR_BGR2GRAY)
                        if cnt == 0:
                            cnt = 1
                        else:
                            mag, ang = processor.opticalFlow(old_gray, cur_gray)
                            all_frames.append(
                                { 'mag': mag
                                , 'ang': ang})
                opticalFlowClips[f] = all_frames
            else:
                if Config.SUBTRACT_BACKGROUND:
                    st = cv2.createBackgroundSubtractorMOG2()
                for c in sorted(listdir(join(Config.DATASET_PATH, f))):
                    if str(join(join(Config.DATASET_PATH, f), c))[-3:] == "tif":
                        img = cv2.imread(join(join(Config.DATASET_PATH, f), c), cv2.COLOR_BGR2GRAY)
                        #img.resize((Config.IMAGE_SHAPE_X, Config.IMAGE_SHAPE_Y))
                        img = cv2.resize(img, (Config.IMAGE_SHAPE_X,Config.IMAGE_SHAPE_Y), interpolation = cv2.INTER_CUBIC)
                        
                        if Config.SUBTRACT_BACKGROUND:
                            img = st.apply(img)
                        # cv2.imshow("fgMask", img)
                        # # cv2.imshow("img", img)
                        # cv2.waitKey()
                        img = np.array(img, dtype=np.float32)
                        img = img / 256.0
                        all_frames.append(img)
                clips.extend(all_frames)
    print("almost done")
    if Config.USE_OPTICAL_FLOW:
        cache["dataset"] = opticalFlowClips
    else:
        cache["dataset"] = clips
    print("one more step")
    cache.close()
    print("stored dataset to cache")
    return np.array(clips)


def get_testset(re=Config.RELOAD_TESTSET, structure = Config.TESTSET_STRUCTURE):
    cache = shelve.open(Config.CACHE_PATH + "testset")
    if not re:
        if Config.CALCULATE_THRESHOLD:
            return get_dataset()
        else:
            if structure == "dict":
                return cache["testset"]
            return  np.array(cache["testset"])
    opticalFlowClips = {}

    def savetocache():
        print("almost done")
        if Config.USE_OPTICAL_FLOW:
            cache["testset"] = opticalFlowClips
        else:
            cache["testset"] = clips
        print("one more step")
        cache.close()
        print("stored testset to cache")
    
    def getAllFrames():
        all_frames = []
        st = cv2.createBackgroundSubtractorMOG2()
        for c in sorted(listdir(join(Config.TESTSET_PATH, f))):
            if str(join(join(Config.TESTSET_PATH, f), c))[-3:] == "tif":
                img = cv2.imread(join(join(Config.TESTSET_PATH, f), c), cv2.COLOR_BGR2GRAY)
                img = cv2.resize(img, (Config.IMAGE_SHAPE_X,Config.IMAGE_SHAPE_Y), interpolation = cv2.INTER_CUBIC)
                if Config.SUBTRACT_BACKGROUND:
                    img = st.apply(img)
                # img.resize((Config.IMAGE_SHAPE_X, Config.IMAGE_SHAPE_Y)) WRONG CODE!!!!!!!!!!!!!!
                # cv2.imshow("img allframe", img)
                # cv2.waitKey()
                img = np.array(img, dtype=np.float32)
                img = img / 256.0
                if Config.MODEL_NAME == "lstm_autoencoder":
                    img.resize((Config.IMAGE_SHAPE_X*Config.IMAGE_SHAPE_Y))
                all_frames.append(img)
        return all_frames
    
    def getAllOpticalFlowFrames():
        cnt = 0
        cur_gray = None
        all_frames = []
        for c in sorted(listdir(join(Config.TESTSET_PATH, f))):
            if str(join(join(Config.TESTSET_PATH, f), c))[-3:] == "tif":
                old_gray = cur_gray
                cur_gray = cv2.imread(join(join(Config.TESTSET_PATH, f), c), cv2.COLOR_BGR2GRAY)
                if cnt == 0:
                    cnt = 1
                else:
                    mag, ang = processor.opticalFlow(old_gray, cur_gray)
                    all_frames.append(
                        { 'mag': mag
                        , 'ang': ang})
        opticalFlowClips[f] = all_frames

    if structure == "dict":
        clips = {}
        for f in sorted(listdir(Config.TESTSET_PATH)):
            if isdir(join(Config.TESTSET_PATH, f)):
                print(f)
                if Config.USE_OPTICAL_FLOW:
                    getAllOpticalFlowFrames()
                else:
                    all_frames = getAllFrames()
                    clips[f] = np.array(all_frames)
        savetocache()
        return clips
    else:
        clips = []
        for f in sorted(listdir(Config.TESTSET_PATH)):
            if isdir(join(Config.TESTSET_PATH, f)):
                print(f)
                if Config.USE_OPTICAL_FLOW:
                    getAllOpticalFlowFrames()
                else:
                    all_frames = getAllFrames()
                    clips.extend(all_frames)
        savetocache()
        return np.array(clips)


def get_single_frame(filename, single_test_case_name, test_set_path):
    path = Config.TESTSET_PATH +"/" + single_test_case_name + "/" + filename
    img = cv2.imread(path, cv2.COLOR_BGR2GRAY)
    img = cv2.resize(img, (Config.IMAGE_SHAPE_X,Config.IMAGE_SHAPE_Y), interpolation = cv2.INTER_CUBIC)
    # img.resize((Config.IMAGE_SHAPE_X, Config.IMAGE_SHAPE_Y))
    img = np.array(img, dtype=np.float32)
    img = img / 256.0
    return img

def getBinarizedOpticalFlowFrames (reloadDataset):
    cache = shelve.open(Config.CACHE_PATH + "datasetBinarizedOpticalFlowFrames")
    if not reloadDataset:
          return cache["datasetBinarizedOpticalFlowFrames"]
    all_frames_mag = []
    all_frames_ang = []
    all_frames_opt = []
    cnt = 0
    for f in sorted(listdir(Config.DATASET_PATH)):
        if isdir(join(Config.DATASET_PATH, f)):
            print(f)
            frames_mag = []
            frames_opt = []
            frames_ang = []
            cnt = 0
            cur_gray = None
            st = cv2.createBackgroundSubtractorMOG2()
            for c in sorted(listdir(join(Config.DATASET_PATH, f))):
                if str(join(join(Config.DATASET_PATH, f), c))[-3:] == "tif":
                    old_gray = cur_gray
                    cur_gray = cv2.imread(join(join(Config.DATASET_PATH, f), c), cv2.COLOR_BGR2GRAY)
                    cur_gray = cv2.resize(cur_gray, (Config.IMAGE_SHAPE_X, Config.IMAGE_SHAPE_Y), interpolation = cv2.INTER_CUBIC)
                    
                    # cur_gray.resize((Config.IMAGE_SHAPE_X, Config.IMAGE_SHAPE_Y)) (this chopes off the remining part WRONG CODE ALERT!!!!!!!!!)
                    #print("shape of cur gray", np.shape(cur_gray))
                    cur_gray = np.array(cur_gray, dtype=np.float32)
                    #cv2.imshow("cur_gray", cur_gray)
                    #cur_gray = cur_gray / 256.0
                    fgMask = st.apply(cur_gray)
                    cv2.imshow("fgMask", fgMask)
                    #print("shape of fgmask", np.shape(fgMask))
                    cv2.waitKey()
                    if cnt == 0:
                        cnt = 1
                    else:
                        mag, ang = processor.opticalFlow(old_gray, cur_gray)
                        mag, ang = processor.binarization(ang, mag, fgMask)
                        frames_opt.append(np.dstack((mag, ang)))
                        # frames_mag.append(mag)
                        # frames_ang.append(ang)
                
            # all_frames_mag.append(frames_mag)
            # all_frames_ang.append(frames_ang)
            all_frames_opt.extend(frames_opt)
            print("shape of output", np.shape(all_frames_opt))
    print("almost done")
    cache["datasetBinarizedOpticalFlowFrames"] = all_frames_opt
    print("one more step")
    cache.close()
    print("stored dataset to cache")
    print("shape of final dataset", np.shape(all_frames_opt))
    return all_frames_opt
