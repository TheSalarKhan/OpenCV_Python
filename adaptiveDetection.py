import cv2
import numpy as np


def nothing(x):
    pass


def tb1(val):
    print val

def tb2(val):
    print val

def tb3(val):
    print val


# Initialize the camera
cap = cv2.VideoCapture(0)
_,frame = cap.read()


height,width,_ = frame.shape

y = height/2
x = width/2

# Starting point for the square's diagonal
start = (x-15,y-15)

# Ending point for the squares diagonal
end = (x+15,y+15)

sx,sy = start
ex,ey = end




cv2.namedWindow('image')



# Creating track bar
cv2.createTrackbar('ht', 'image',0,179,tb1)
cv2.createTrackbar('st', 'image',0,255,tb2)
cv2.createTrackbar('vt', 'image',0,255,tb3)

locked = False

# this is the average color to detect
h,s,v = (0,0,0)


while(1):

    # Read a frame from the camera
    _, frame = cap.read()

    # Blur the image for filtering
    frame = cv2.GaussianBlur(frame,(3,3),0)

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # If the user has not locked the colot
    if(locked == False):
        # pick the reigon inside the square
        reigonOfInterest = hsv[(sy+1):(ey-1),(sx+1):(ex-1)]

        # get the HSV values for the average color
        # in the reigon of interest
        h,s,v,_ =  cv2.mean(reigonOfInterest)
        # color = np.uint8([[[b,g,r]]])
        # color = cv2.cvtColor(color, cv2.COLOR_BGR2HSV)
        
        

    # get the values from the trackbars on the image
    ht = cv2.getTrackbarPos('ht','image')
    st = cv2.getTrackbarPos('st','image')
    vt = cv2.getTrackbarPos('vt','image')

    lower = np.array([h-ht,s-st,v-vt])
    upper = np.array([h+ht,s+st,v+vt])


    

    mask = cv2.inRange(hsv,lower,upper)

    cv2.imshow('mask',mask)
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

        





    
    

    # Draw a rectangle in the center
    frame = cv2.rectangle(frame,start,end,(0,255,0),1)

    if(ci != -1):
        # Find and draw the hull around the largest contour
        hull = cv2.convexHull(cnt)
        cv2.drawContours(frame,[hull],0,(0,255,0),2)
    
    cv2.imshow('image',frame)

    
    k = cv2.waitKey(5) & 0xFF

    

    if k == 27:
        break
    elif k == ord('l'):
        print 'locked'
        locked = True
    elif k == ord('u'):
        print 'un-locked'
        locked = False
    elif k == ord('c'):
        print 'mask captured'
        cv2.imwrite('mask.png',mask)

cap.release()
cv2.destroyAllWindows()