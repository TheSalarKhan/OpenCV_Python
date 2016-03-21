import numpy as np
import cv2
import os

cv2.namedWindow('controls')


def rgammaChanged(val):
	value = float(val) / 1000.0
	os.system("xgamma -rgamma "+str(value))

def ggammaChanged(val):
	value = float(val) / 1000.0
	os.system("xgamma -bgamma "+str(value))

def bgammaChanged(val):
	value = float(val) / 1000.0
	os.system("xgamma -ggamma "+str(value))

cv2.createTrackbar('rgamma', 'controls',0,10000,rgammaChanged)
cv2.createTrackbar('ggamma', 'controls',0,10000,ggammaChanged)
cv2.createTrackbar('bgamma', 'controls',0,10000,bgammaChanged)


cv2.waitKey(0)