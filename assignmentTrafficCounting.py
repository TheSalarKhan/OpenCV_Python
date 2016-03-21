import numpy as np
import cv2
from Camera import Camera

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
    # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return frame

camera = cv2.VideoCapture('traffic.mp4')

ALPHA = 0.01


reigon1 = ROI((0,40,300,150))
_,fr = camera.read()
fr = reigon1.getROI(fr)

BG = denoise(cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY))



# c =1
while True:
    ret,frame = camera.read()
    # frame = frame[]

    if ret is True:
        frame = reigon1.getROI(frame)

        f = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

        BG = f * ALPHA + BG * (1 - ALPHA)


        mask = cv2.absdiff(f.astype(np.uint8), BG.astype(np.uint8))

        ret, mask = cv2.threshold(mask.astype(np.uint8), 40, 255, cv2.THRESH_BINARY)

        # disc = cv2.getStructuringElement(cv2.MORPH_RECT,(7,7))
        
        # cv2.filter2D(mask,-1,disc,mask)

        kernel = np.ones((3,3),np.uint8)
        mask = cv2.erode(mask,kernel,iterations = 1)
        # mask = cv2.dilate(mask,np.ones((11,11),np.uint8),iterations = 1)

        # Now convolute with circular disc
        disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(11,11))
        cv2.filter2D(mask,-1,disc,mask)

        # reigon1.drawBoundary(frame)
        cv2.imshow('fore', mask)
        

        _,contours,_ = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)

        # get the contour with the greatest area
        # max_area = -1
        # ci = -1
        for i in range(len(contours)):
            cnt=contours[i]
            area = cv2.contourArea(cnt)

            if area > 45:
                hull = cv2.convexHull(cnt)
                cv2.drawContours(frame,[hull],0,(0,255,0),2)
            
            # if(area>max_area):
            #     max_area=area
            #     ci=i

        # if(ci != -1):
        #     cnt=contours[ci]

        # # cv2.imshow('mask',mask)

        # # Draw a rectangle in the center
        # frame = cv2.rectangle(frame,params.start,params.end,(0,255,0),1)

        # if(ci != -1):
            # Find and draw the hull around the largest contour
            

        cv2.imshow('image',frame)



        # print frame.astype(int)
        # print BG.astype(int)

        # c = c+1

    key = cv2.waitKey(10) & 0xFF
    if key == 27:
      break

camera.release()
cv2.destroyAllWindows()