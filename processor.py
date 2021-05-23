import cv2
import numpy as np

def opticalFlow(old_frame, cur_frame, cvtToDegree=False, normalise=False):
    old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
    cur_gray = cv2.cvtColor(cur_frame, cv2.COLOR_BGR2GRAY)
    flow = cv2.calcOpticalFlowFarneback(old_gray, cur_gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)
    mag, ang = cv2.cartToPolar(flow[...,0], flow[...,1])
    if cvtToDegree:
        ang = ang*180/np.pi
    if normalise:
        mag = cv2.normalize(mag,None,0,255,cv2.NORM_MINMAX) #Need to Confirm
    return mag, ang
