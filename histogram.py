import cv2
import numpy as np
import time


 
roi = cv2.imread('roi.png')
hsv = cv2.cvtColor(roi,cv2.COLOR_BGR2HSV)
 
target = cv2.imread('frame.png')
hsvt = cv2.cvtColor(target,cv2.COLOR_BGR2HSV)

start_time = time.time()
 
# calculating object histogram
roihist = cv2.calcHist([hsv],[0, 1], None, [180, 256], [0, 180, 0, 256] )


# normalize histogram and apply backprojection
cv2.normalize(roihist,roihist,0,255,cv2.NORM_MINMAX)
dst = cv2.calcBackProject([hsvt],[0,1],roihist,[0,180,0,256],100)
 
# Now convolute with circular disc
disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
cv2.filter2D(dst,-1,disc,dst)
 
# threshold and binary AND
ret,thresh = cv2.threshold(dst,50,255,0)
# thresh = cv2.merge((thresh,thresh,thresh))
# res = cv2.bitwise_and(target,thresh)

print("--- %s seconds ---" % (time.time() - start_time))
 
cv2.imshow('res',thresh)

cv2.waitKey(0)