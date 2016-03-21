import cv2
import numpy as np


frame = cv2.imread('frame.png',0)
avg1 = cv2.imread('avg1.png',0)
avg2 = cv2.imread('avg2.png',0)

# apply gaussian blur
frame = cv2.GaussianBlur(frame,(5,5),0)
avg1 = cv2.GaussianBlur(avg1,(5,5),0)
avg2 = cv2.GaussianBlur(avg2,(5,5),0)

cv2.imshow('frame',frame)
# cv2.imshow('avg1',avg1)
cv2.imshow('avg2',avg2)
cv2.imshow('subt',frame - avg2)

# print frame.dtype

# frame = np.array(
#     [[0,255,255,255,255,255],
#     [255,255,255,255,255,255],
#     [255,255,255,255,255,255],
#     [255,255,255,255,255,255],
#     [255,255,255,255,255,255],
#     [255,255,255,255,255,255],
#     [255,255,255,255,255,255]], dtype=np.uint8)



# sub = np.where(frame > 1,1,0)
# subtracted = frame - avg2

# # subtracted = np.where(np.absolute(subtracted) > 0,255,0)

# subtracted = np.where(subtracted > 128,255,0)
# subtracted = subtracted.astype('uint8')

# # print subtracted.shape

# cv2.imshow('binary',frame & subtracted)

# cv2.imshow('frame',frame - avg2)
# cv2.imshow('fram2e',frame - avg1)
# cv2.imshow('avg1',avg1)
# cv2.imshow('avg2',avg2)

cv2.waitKey(0)


cv2.destroyAllWindows()
 
# c = cv2.VideoCapture(0)
# _,f = c.read()

# f = cv2.cvtColor(f,cv2.COLOR_BGR2GRAY)

 
# avg1 = np.float32(f)
# avg2 = np.float32(f)
 
# while(1):
#     _,f = c.read()

#     f = cv2.cvtColor(f,cv2.COLOR_BGR2GRAY)
     
#     cv2.accumulateWeighted(f,avg1,0.1)
#     cv2.accumulateWeighted(f,avg2,0.01)
     
#     res1 = cv2.convertScaleAbs(avg1)
#     res2 = cv2.convertScaleAbs(avg2)


#     binary = np.where( (f - res2) > -2, 1,0)  
 
#     cv2.imshow('img',binary)
#     cv2.imshow('avg1',res1)
#     cv2.imshow('avg2',res2)
#     k = cv2.waitKey(20) & 0xFF
 
#     if k == ord('q'):
#         break
 
# cv2.destroyAllWindows()
# c.release()
