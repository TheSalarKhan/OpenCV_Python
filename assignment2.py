import numpy as np
from collections import deque
import cv2
from Camera import Camera

VIDEO_SOURCE = 0

# class ROI:
# 	def __init__(self,center,size):
# 		x = center[0]
# 		y = center[1]
		
# 		self.start = (x-size,y-size)
# 		self.end   = (x+size,y+size)

# 	def drawBoundary(self,frame):
# 		cv2.rectangle(frame,self.start,self.end,(0,255,0),1)

# 	def getROI(self,frame):
# 		return frame[ self.start[1]:self.end[1] , self.start[0]:self.end[0] ]

class ROI:
	def __init__(self,track_window):
		x = track_window[0]
		y = track_window[1]

		width = track_window[2]
		height = track_window[3]
		
		self.start = (x,y)
		self.end   = (x+width,y+height)

	def drawBoundary(self,frame):
		cv2.rectangle(frame,self.start,self.end,(0,255,0),1)

	def getROI(self,frame):
		return frame[ self.start[1]:self.end[1] , self.start[0]:self.end[0] ]


class Parameters:
	def __init__(self,source=0):
		# Selected base color
		# fourth one is not used
		self.hsv = (0,0,0,0)
		self.hsv2 = (0,0,0,0)
		self.hsv3 = (0,0,0,0)


		# Thresholds
		self.ht = 0
		self.st = 180
		self.vt = 200
		self.ht_ = 0
		self.st_ = 180
		self.vt_ = 200
		
		# Co-ords for the color selection square
		# self.start = (0,0)
		# self.end   = (0,0)
		self.center = (0,0)

		# Boolean to check weather
		# the colors are locked or not
		self.locked = False

		# Get the camera object
		self.cam = Camera(source)

	def findCenter(self):
		# Read a frame
		frame = self.cam.read()

		# Calculate the co-ordinates for the center pixel
		y = frame.shape[0]/2
		x = frame.shape[1]/2

		self.center = (x,y)



params = Parameters(VIDEO_SOURCE)

# get the co-ords for the square in the center
params.findCenter()




track_window = (params.center[1],params.center[0],20,20)

reigon1 = ROI(track_window)

reigon2 = None


# reigon2 = ROI((params.center[0]+5,params.center[1]),5)
# reigon3 = ROI((params.center[0]-5,params.center[1]-5),5)
roi_hist = None
term_crit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 20, 1 )


while(True):
	# Read a frame from the camera
	frame = params.cam.read()



	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	cv2.medianBlur(hsv,5)
	cv2.GaussianBlur(hsv,(5,5),0)

	if params.locked is not True:
		hsv_roi = reigon1.getROI(hsv)
		roi_hist = cv2.calcHist([hsv_roi],[0,1],None,[180,255],[0,180,0,255])
		cv2.normalize(roi_hist,roi_hist,0,255,cv2.NORM_MINMAX)


	

	

	dst = cv2.calcBackProject([hsv],[0,1],roi_hist,[0,180,0,255],1)

	cv2.imshow('dst',cv2.flip(dst,1))

    # apply meanshift to get the new location
	ret, track_window = cv2.meanShift(dst, track_window, term_crit)


	reigon2 = ROI(track_window)


	reigon2.drawBoundary(frame)
	reigon1.drawBoundary(frame)

	cv2.imshow('output',cv2.flip(frame,1))


	
	k = cv2.waitKey(60) & 0xFF
	
	if k == 27:
		break
	elif k == ord('l'):
	    print 'locked'
	    params.locked = True
	elif k == ord('u'):
	    print 'un-locked'
	    params.locked = False
	# elif k == ord('c'):
	#     # print 'mask captured'
	#     # cv2.imwrite('mask.png',mask)

params.cam.stop()
cv2.destroyAllWindows()