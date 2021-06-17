import cv2
import numpy as np


def opticalFlow(old_frame, cur_frame, cvtToDegree=False, normalise=False, cvtToGray = False):
    if cvtToGray :
        old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
        cur_gray = cv2.cvtColor(cur_frame, cv2.COLOR_BGR2GRAY)
    else:
        old_gray = old_frame
        cur_gray = cur_frame 
    flow = cv2.calcOpticalFlowFarneback(old_gray, cur_gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)
    mag, ang = cv2.cartToPolar(flow[...,0], flow[...,1])
    if cvtToDegree:
        ang = ang*180/np.pi
    if normalise:
        mag = cv2.normalize(mag,None,0,255,cv2.NORM_MINMAX) #Need to Confirm
    return mag, ang

def binarization(ang, mag, fgMask):
    #print("binarizing")
    for i in range(len(fgMask)):
        for j in range(len(fgMask[0])):
            if fgMask[i][j] == 0:
                ang[i][j] = 0
                mag[i][j] = 0
    return mag, ang
