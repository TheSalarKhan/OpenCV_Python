import numpy as np
from collections import deque
import cv2
from Camera import Camera

VIDEO_SOURCE = 0

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

def threshChanged1(val):
	params.ht = val

def threshChanged2(val):
	params.st = val

def threshChanged3(val):
	params.vt = val

def threshChanged4(val):
	params.ht_ = val

def threshChanged5(val):
	params.st_ = val

def threshChanged6(val):
	params.vt_ = val

params = Parameters(VIDEO_SOURCE)

# get the co-ords for the square in the center
params.findCenter()

# Create an output window
cv2.namedWindow('controls')


# Create trackbars in the output window
cv2.createTrackbar('h+', 'controls',0,179,threshChanged1)
cv2.createTrackbar('s+', 'controls',0,255,threshChanged2)
cv2.createTrackbar('v+', 'controls',0,255,threshChanged3)
cv2.createTrackbar('h-', 'controls',0,179,threshChanged4)
cv2.createTrackbar('s-', 'controls',0,255,threshChanged5)
cv2.createTrackbar('v-', 'controls',0,255,threshChanged6)

# cam = cv2.VideoCapture(VIDEO_SOURCE)

# roihist = None








pts = deque(maxlen=100000)

def getMask(frame,hsv):

	lower = np.array([0,0,0], dtype=np.uint8)
	upper = np.array([0,0,0], dtype=np.uint8)
	

	lower[0] = hsv[0]-params.ht_
	lower[1] = hsv[1]-params.st_
	lower[2] = 0

	upper[0] = hsv[0]+params.ht
	upper[1] = hsv[1]+params.st
	upper[2] = 255

	return cv2.inRange(frame,lower,upper)

track_window = (params.center[1],params.center[0],50,50)

reigon1 = ROI(track_window)
reigon2 = None
# reigon2 = ROI((params.center[0]+5,params.center[1]),5)
# reigon3 = ROI((params.center[0]-5,params.center[1]-5),5)

term_crit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 20, 1 )

while(True):
	# Read a frame from the camera
	frame = params.cam.read()
	
	# reigon2.drawBoundary(frame)

	# Convert to hsv space
	hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
	# hsv = frame

	# # # Blur the image for filtering
	cv2.medianBlur(hsv,5)
	cv2.GaussianBlur(hsv,(5,5),0)
	


	if not params.locked:
		# Calculate average color
		params.hsv = cv2.mean(reigon1.getROI(hsv))
		# params.hsv2 = cv2.mean(reigon2.getROI(hsv))
		# params.hsv3 = cv2.mean(reigon3.getROI(hsv))



	mask = getMask(hsv,params.hsv)
	# mask = mask + getMask(hsv,params.hsv2) 
	# mask = mask + getMask(hsv,params.hsv3)

	disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(7,7))
	
	cv2.filter2D(mask,-1,disc,mask)

	# apply meanshift to get the new location
	ret, track_window = cv2.CamShift(mask, track_window, term_crit)


	reigon2 = ROI(track_window)
	


	

	cv2.imshow('mask1',cv2.flip(mask,1))
	# cv2.imshow('mask2',mask2)
	# cv2.imshow('mask3',mask3)




	reigon1.drawBoundary(frame)

	if reigon2 is not None:
		reigon2.drawBoundary(frame)
	# reigon2.drawBoundary(frame)
	# reigon3.drawBoundary(frame)
	# cv2.imshow('original',frame)

	# _,contours,_ = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)


	# # get the contour with the greatest area
	# cnt=None
	# center = None
	# max_area = -1
	# ci = -1
	# for i in range(len(contours)):
	#     cnt=contours[i]
	#     area = cv2.contourArea(cnt)
	#     if(area>max_area):
	#         max_area=area
	#         ci=i

	# if(ci != -1):
	#     cnt=contours[ci]
    
	# # cv2.imshow('mask',mask)

	# # # Draw a rectangle in the center
	# # frame = cv2.rectangle(frame,params.start,params.end,(0,255,0),1)

	# if(ci != -1):
	#     # Find and draw the hull around the largest contour
	#     hull = cv2.convexHull(cnt)
	#     cv2.drawContours(frame,[hull],0,(0,255,0),2)
   
 #    # only proceed if at least one contour was found

	# if len(contours) > 0:
		
	# 	# find the largest contour in the mask, then use
	# 	# it to compute the minimum enclosing circle and
	# 	# centroid
	# 	c=np.array(cnt)
	# 	#print(c)

	# 	#c = max(cnt, key=cv2.contourArea)
		
	# 	M = cv2.moments(c)
	# 	center = (int(M["m10"]/ M["m00"] ), int(M["m01"]/ M["m00"]))

 
     
	# # update the points queue
	# if(params.locked is True):
	# 	pts.appendleft(center)

	
	
	# 	# loop over the set of tracked points
	# for i in xrange(1, len(pts)):
	# 	# if either of the tracked points are None, ignore
	# 	# them
	# 	if pts[i - 1] is None or pts[i] is None:
	# 		continue
 
	# 	# otherwise, compute the thickness of the line andq
	# 	# draw the connecting lines
	# 	#thickness = float(np.sqrt(100000 / float(i + 1)) * 2.5)
	# 	if(params.locked is True):

	# 		cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), 2)


		
 
	# show the frame to our screen
	cv2.imshow("Frame", cv2.flip(frame,1))
	


	k = cv2.waitKey(5) & 0xFF

	if k == 27:
	    break
	elif k == ord('l'):
	    print 'locked'
	    params.locked = True
	elif k == ord('u'):
	    print 'un-locked'
	    params.locked = False
	elif k == ord('c'):
	    print 'mask captured'
	    cv2.imwrite('mask.png',mask)


params.cam.stop()
cv2.destroyAllWindows()





