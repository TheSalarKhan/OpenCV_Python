import numpy as np
import cv2
from Camera import Camera

def denoise(frame):
    frame = cv2.medianBlur(frame,5)
    frame = cv2.GaussianBlur(frame,(5,5),0)
    # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return frame

camera = Camera(0)

ALPHA = 0.015

BG = denoise(cv2.cvtColor(camera.read(), cv2.COLOR_BGR2GRAY))



# c =1
while True:
    frame = camera.read()

    f = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    BG = f * ALPHA + BG * (1 - ALPHA)


    mask = cv2.absdiff(f.astype(np.uint8), BG.astype(np.uint8))

    ret, mask = cv2.threshold(mask.astype(np.uint8), 15, 255, cv2.THRESH_BINARY)

    # disc = cv2.getStructuringElement(cv2.MORPH_RECT,(7,7))
    
    # cv2.filter2D(mask,-1,disc,mask)

    cv2.imshow('fore', mask)
    

    _,contours,_ = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)

    # get the contour with the greatest area
    max_area = -1
    ci = -1
    for i in range(len(contours)):
        cnt=contours[i]
        area = cv2.contourArea(cnt)
        if(area>max_area):
            max_area=area
            ci=i

    if(ci != -1):
        cnt=contours[ci]

    # # cv2.imshow('mask',mask)

    # # Draw a rectangle in the center
    # frame = cv2.rectangle(frame,params.start,params.end,(0,255,0),1)

    if(ci != -1):
        # Find and draw the hull around the largest contour
        hull = cv2.convexHull(cnt)
        cv2.drawContours(frame,[hull],0,(0,255,0),2)

    cv2.imshow('image',frame)



    # print frame.astype(int)
    # print BG.astype(int)

    # c = c+1

    key = cv2.waitKey(10) & 0xFF
    if key == 27:
      break

camera.stop()
cv2.destroyAllWindows()