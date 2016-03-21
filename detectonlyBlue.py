import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while(1):

    # Take each frame
    _, frame = cap.read()

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # define range of blue color in HSV
    lower_blue = np.array([110,50,50])
    upper_blue = np.array([130,255,255])

    # # Lower and upper bounds for skin color
    # lower_blue = np.array([0,48,80])
    # upper_blue = np.array([20,255,255])

    # Threshold the HSV image to get only blue colors
    mask = cv2.medianBlur(cv2.inRange(hsv, lower_blue, upper_blue),3);


    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame,frame, mask= mask)

    # cv2.imshow('frame',frame)
    cv2.imshow('mask',cv2.flip(mask,1))
    cv2.imshow('res',cv2.flip(res,1))
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
