import numpy as np
import cv2
from collections import deque

class BackGroundSubtractor:
	# When constructing background subtractor, we
	# take in two arguments:
	# 1) alpha: The background learning factor, its value should
	# be between 0 and 1. The higher the value, the more quickly
	# your algorithm learns the changes in the background. Therefore, 
	# for a static background use a lower value, like 0.001. But if 
	# your background has moving trees and stuff, use a higher value,
	# maybe start with 0.01.
	# 2) firstFrame: This is the first frame from the video/webcam.
	def __init__(self,alpha,firstFrame):
		self.alpha  = alpha
		self.backGroundModel = firstFrame
		self.lockModel = False

	def getForeground(self,frame,threshold=(20,255)):

		mask = self.getMask(frame,threshold)

		fg = cv2.bitwise_and(frame,frame,mask = mask)

		return fg

	def lockBG(self):
		self.lockModel = True

	def lockBG(self):
		self.lockModel = False

	def getMask(self,frame,threshold):

		# Learn the new frame only if the model is not locked
		if self.lockModel is False:
			# apply the background averaging formula:
			# NEW_BACKGROUND = CURRENT_FRAME * ALPHA + OLD_BACKGROUND * (1 - APLHA)
			self.backGroundModel =  frame * self.alpha + self.backGroundModel * (1 - self.alpha)

		# after the previous operation, the dtype of
		# self.backGroundModel will be changed to a float type
		# therefore we do not pass it to cv2.absdiff directly,
		# instead we acquire a copy of it in the uint8 dtype
		# and pass that to absdiff.

		maskRGB = cv2.absdiff(self.backGroundModel.astype(np.uint8),frame)

		mask = cv2.cvtColor(maskRGB,cv2.COLOR_BGR2GRAY)

		# Apply thresholding on the background and display the resulting mask
		_, mask = cv2.threshold(mask, threshold[0], threshold[1], cv2.THRESH_BINARY)

		return mask

	def getModel(self):
		return self.backGroundModel.astype(np.uint8)

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

def denoise(frame):
    frame = cv2.medianBlur(frame,5)
    frame = cv2.GaussianBlur(frame,(5,5),0)
    
    return frame

def findCenter(frame):
	# Calculate the co-ordinates for the center pixel
	y = frame.shape[0]/2
	x = frame.shape[1]/2

	return (x,y)

def getObject(frame,hsv):

	lower = np.array([0,0,0], dtype=np.uint8)
	upper = np.array([0,0,0], dtype=np.uint8)
	

	lower[0] = hsv[0]-2
	lower[1] = hsv[1]-30
	lower[2] = 0

	upper[0] = hsv[0]+2
	upper[1] = hsv[1]+40
	upper[2] = 255

	return cv2.inRange(frame,lower,upper)


pts = deque(maxlen=100000)
def drawLines(obj,frame):
	#########################################################################
	_,contours,_ = cv2.findContours(obj,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)

	# get the contour with the greatest area
	cnt=None
	center = None
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

	# cv2.imshow('mask',mask)

	# # Draw a rectangle in the center
	# frame = cv2.rectangle(frame,params.start,params.end,(0,255,0),1)

	if(ci != -1):
	    # Find and draw the hull around the largest contour
	    hull = cv2.convexHull(cnt)
	    cv2.drawContours(frame,[hull],0,(0,255,0),2)

	# only proceed if at least one contour was found

	if len(contours) > 0:
		
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
		c=np.array(cnt)
		#print(c)

		#c = max(cnt, key=cv2.contourArea)
		
		M = cv2.moments(c)
		center = (int(M["m10"]/ M["m00"] ), int(M["m01"]/ M["m00"]))

		# update the points queue
		if(LOCKED is True):
			pts.appendleft(center)



		# loop over the set of tracked points
	for i in xrange(1, len(pts)):
		# if either of the tracked points are None, ignore
		# them
		if pts[i - 1] is None or pts[i] is None:
			continue

		# otherwise, compute the thickness of the line andq
		# draw the connecting lines
		#thickness = float(np.sqrt(100000 / float(i + 1)) * 2.5)
		if(LOCKED is True):
			cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), 2)
	####################################################################################
##################################################################################################


LOCKED = False
center = (0,0)
HSV = (0,0,0)
# x, y, width, height
trackWindow = (0,0,0,0)

reigon1 = ROI(trackWindow)

cam = cv2.VideoCapture(0)

ret,frame = cam.read()
if ret is True:
	center = findCenter(frame)
	trackWindow = (center[1],center[0],15,15)
	reigon1 = ROI(trackWindow)
	backSubtractor = BackGroundSubtractor(0.005,denoise(frame))
	backSubtractor.lockModel = True
	run = True
else:
	run = False



while(run):
	# Read a frame from the camera
	ret,frame = cam.read()

	frame = denoise(frame)

	# If the frame was properly read.
	if ret is True:
		
		# get the foreground
		fg = backSubtractor.getForeground(frame,(15,255))

		# convert to hsv
		fgHSV = cv2.cvtColor(fg,cv2.COLOR_BGR2HSV)

		if not LOCKED:
			# Convert the frame to HSV
			frameHSV = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
			# Calculate the mean HSV of ROI
			HSV = cv2.mean(reigon1.getROI(frameHSV))

			reigon1.drawBoundary(frame)

		obj = getObject(fgHSV,HSV)

		obj = cv2.erode(obj,np.ones((3,3),np.uint8),iterations = 1)

		disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(7,7))
		cv2.filter2D(obj,-1,disc,obj)

		fg = backSubtractor.getForeground(frame)

		drawLines(obj.copy(),frame)



		cv2.imshow('object',cv2.flip(obj,1))

		cv2.imshow('frame',cv2.flip(frame,1))

		cv2.imshow('model',cv2.flip(fg,1))



		key = cv2.waitKey(10) & 0xFF
		
		if key == 27:
			break
		elif key == ord('l'):
			LOCKED = True
			backSubtractor = BackGroundSubtractor(0.1,frame)
		elif key == ord('u'):
			LOCKED = False

		elif key == ord('b'):
			# Toggle background averaging state
			backSubtractor.lockModel = not backSubtractor.lockModel
			if backSubtractor.lockModel is True:
				print 'BG locked'
			else:
				print 'BG unlocked'

		elif key == ord('c'):
			pts = deque(maxlen=100000)
	else:
		break

	

cam.release()
cv2.destroyAllWindows()