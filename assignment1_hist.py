import numpy as np
import cv2
from Camera import Camera


class Application:
	def __init__(self,source=0):
		self.START = None
		self.END   = None
		self.CAM = Camera(source)
		self.LOCKED = False
		self.ROI_HIST = None

	def findCenter(self):
		# Read a frame
		frame = self.CAM.read()

		# Calculate the co-ordinates for the center pixel
		y = frame.shape[0]/2
		x = frame.shape[1]/2

		# Calculate the points for the
		# diagonal of the square
		# which will be displayed in the center
		self.START = ( x-25 , y-25 )
		self.END   = ( x+25 , y+25 )

	def run(self):
		self.findCenter()

		while True:
			# Read a frame from the camera
			frame = self.CAM.read()

			

			# b,g,r = cv2.split(frame)

			# b = cv2.equalizeHist(b)
			# g = cv2.equalizeHist(g)
			# r = cv2.equalizeHist(r)

			# frame = cv2.merge((b,g,r))


			# frame = cv2.GaussianBlur(frame,(3,3),0)
			# frame = cv2.medianBlur(frame,3)

			# Convert to hsv format
			# hsv = frame
			hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
			# hsv = cv2.split(frame)[2]

			
			

			if not self.LOCKED:
				# Get the reigon of interest
				reigonOfInterest = hsv[ self.START[1]:self.END[1],self.START[0]:self.END[0],]
				
				# Calculate histogram
				self.ROI_HIST = cv2.calcHist([reigonOfInterest],[0,1], None, [180,255], [0,180,0, 255] )

			# Normalize the histogram
			cv2.normalize(self.ROI_HIST,self.ROI_HIST,0,255,cv2.NORM_MINMAX)
			
			# Calculate back projection
			dst = cv2.calcBackProject([hsv],[0,1],self.ROI_HIST,[0,180,0,255],10)
			 
			# Now convolute with circular disc
			


			 
			# threshold

			# kernel = np.ones((5,5),np.uint8)

			


			

			# ret,mask = cv2.threshold(dst,50,255,0)
			
			

			# disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
			# cv2.filter2D(dst,-1,disc,dst)


			# dst = cv2.merge((dst,dst,dst))
			# res = cv2.bitwise_and(frame,dst)

			# disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
			# cv2.filter2D(dst,-1,disc,dst)

			# # dst = cv2.morphologyEx(dst,cv2.MORPH_OPEN,kernel)

			# # dst = cv2.morphologyEx(dst,cv2.MORPH_OPEN,kernel)

			# # dst = cv2.morphologyEx(dst,cv2.MORPH_OPEN,kernel)

			# # dst = cv2.morphologyEx(dst,cv2.MORPH_CLOSE,kernel)

			# # dst = cv2.morphologyEx(dst,cv2.MORPH_CLOSE,kernel)

			# dst = cv2.morphologyEx(dst,cv2.MORPH_CLOSE,kernel)

			# dst = cv2.morphologyEx(dst,cv2.MORPH_CLOSE,kernel)


			# show the frame
			# dst = cv2.dilate(dst,np.ones((3,3),np.uint8),iterations=2)
			cv2.imshow('mask',dst)


			cv2.rectangle(frame,self.START,self.END,(0,255,0),1)
			cv2.imshow('original',frame)



			# Lookout for any key presses
			key = cv2.waitKey(1) & 0xFF
			if key == 27:
				break
			if key == ord('l'):
				self.LOCKED = True
			if key == ord('u'):
				self.LOCKED = False

		self.end()


	def end(self):
		self.CAM.stop()
		cv2.destroyAllWindows()


app = Application(0)

app.run()
# while(True):

# 	# start_time = time.time()
# 	# Read a frame from the camera
# 	_,frame = cam.read()

# 	# Convert to hsv space
# 	hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

# 	# # # Blur the image for filtering
# 	hsv = cv2.GaussianBlur(hsv,(3,3),0)
# 	hsv = cv2.medianBlur(hsv,3)

	

# 	if not params.locked:
# 		# pick the reigon of interest
# 		reigonOfInterest = hsv[\
# 			params.start[1]:params.end[1], \
# 			params.start[0]:params.end[0], \
# 		]

# 		# calculating object histogram
# 		roihist = cv2.calcHist([reigonOfInterest],[0, 1], None, [180, 256], [0, 180, 0, 256] )


# 	# normalize histogram and apply backprojection
	



# 	# print("--- %s seconds ---" % (time.time() - start_time))

# 	_,contours,_ = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)

# 	# get the contour with the greatest area
# 	max_area = -1
# 	ci = -1
# 	for i in range(len(contours)):
# 	    cnt=contours[i]
# 	    area = cv2.contourArea(cnt)
# 	    if(area>max_area):
# 	        max_area=area
# 	        ci=i

# 	if(ci != -1):
# 	    cnt=contours[ci]

# 	# cv2.imshow('mask',mask)

# 	# Draw a rectangle in the center
# 	frame = cv2.rectangle(frame,params.start,params.end,(0,255,0),1)

# 	if(ci != -1):
# 	    # Find and draw the hull around the largest contour
# 	    hull = cv2.convexHull(cnt)
# 	    cv2.drawContours(frame,[hull],0,(0,255,0),2)

# 	cv2.imshow('image',frame)
	


# 	k = cv2.waitKey(5) & 0xFF

# 	if k == 27:
# 	    break
# 	elif k == ord('l'):
# 	    print 'locked'
# 	    params.locked = True
# 	elif k == ord('u'):
# 	    print 'un-locked'
# 	    params.locked = False
# 	elif k == ord('c'):
# 	    print 'mask captured'
# 	    cv2.imwrite('mask.png',mask)


# cam.release()
# cv2.destroyAllWindows()





