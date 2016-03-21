import numpy as np
import cv2

img = cv2.imread('mask.png')

img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

# cv2.imshow('result',img)

image,contours,hierarchy = cv2.findContours(img.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)

# max_area = -1
# for i in range(len(contours)):
#     cnt=contours[i]
#     area = cv2.contourArea(cnt)
#     if(area>max_area):
#         max_area=area
#         ci=i
# cnt=contours[ci]

# print cnt
# Get the bounding rectangle
# x,y,w,h = cv2.boundingRect(cnt)


# cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),5)




img = cv2.drawContours(image,contours,-1,(255,0,0),4)

image,contours,hierarchy = cv2.findContours(img.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
img = cv2.drawContours(image,contours,-1,(255,0,0),4)


hull = cv2.convexHull(contours[])
cv2.drawContours(img,[hull],0,(255,0,0),2)


# hull = cv2.convexHull(contours[0])



cv2.imshow('result',img)


cv2.waitKey(0)