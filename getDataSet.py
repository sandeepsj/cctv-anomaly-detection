import shelve
from os import listdir
from os.path import join, isdir
import numpy as np
import Config
import cv2
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
                for c in sorted(listdir(join(Config.DATASET_PATH, f))):
                    if str(join(join(Config.DATASET_PATH, f), c))[-3:] == "tif":
                        img = cv2.imread(join(join(Config.DATASET_PATH, f), c), cv2.COLOR_BGR2GRAY)
                        img.resize((128, 128))
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
        for c in sorted(listdir(join(Config.TESTSET_PATH, f))):
            if str(join(join(Config.TESTSET_PATH, f), c))[-3:] == "tif":
                img = cv2.imread(join(join(Config.TESTSET_PATH, f), c), cv2.COLOR_BGR2GRAY)
                img.resize((128, 128))
                img = np.array(img, dtype=np.float32)
                img = img / 256.0
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