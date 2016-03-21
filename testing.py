import numpy as np
import cv2

cam = cv2.VideoCapture(0)

_,frame = cam.read()

print frame.shape