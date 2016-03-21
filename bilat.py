import numpy as np
import cv2


def processFrame(frame,threshold):

	# conver the image to grayscale
	gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

	# apply gaussian blur
	gray = cv2.GaussianBlur(gray,(3,3),0)

	_,gray = cv2.threshold(gray,70,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

	# flip the image for a mirror effect
	gray = cv2.flip(gray,1)
	cv2.imshow('output',gray)


camera = cv2.VideoCapture(0)

while(camera.isOpened()):
	_,currentFrame = camera.read()

	processFrame(currentFrame)

	if (cv2.waitKey(1) & 0xFF == ord('q')):
		break


 # import cv2                             
 # import numpy as np                           #importing libraries
 #                      cap = cv2.VideoCapture(0)                #creating camera object
 #                      while( cap.isOpened() ) :
 #                               ret,img = cap.read()                         #reading the frames
 #                               cv2.imshow('input',img)                  #displaying the frames
 #                               k = cv2.waitKey(10)
 #                               if k == 27:
 #                               break