import numpy as np
import cv2

cam = cv2.VideoCapture(0)

while(True):
	ret,frame = cam.read()

	if ret is True:
		hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

		backToRGB = cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)

		hsv = cv2.cvtColor(backToRGB,cv2.COLOR_BGR2HSV)

		backToRGB = cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)

		hsv = cv2.cvtColor(backToRGB,cv2.COLOR_BGR2HSV)

		backToRGB = cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)

		hsv = cv2.cvtColor(backToRGB,cv2.COLOR_BGR2HSV)

		backToRGB = cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)

		cv2.imshow('output',backToRGB)

		cv2.imshow('original',frame)
	else:
		break

	key = cv2.waitKey(10) & 0xFF

	if key == 27:
		break

cv2.destroyAllWindows()
cam.release()