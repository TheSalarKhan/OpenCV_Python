# Standard imports
import cv2
import numpy as np;


c = cv2.VideoCapture(0)
 
while(1):
    _,f = c.read()

    
    k = cv2.waitKey(20) & 0xFF

    cv2.imshow('frame',f)
 
    if k == ord('q'):
        cv2.imwrite('blob.png',f)
        break



# Read image
im = cv2.imread("blob.png", cv2.IMREAD_GRAYSCALE)
 
# Set up the detector with default parameters.
detector = cv2.SimpleBlobDetector_create()
 
# Detect blobs.
keypoints = detector.detect(im)
 
# Draw detected blobs as red circles.
# cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
im_with_keypoints = cv2.drawKeypoints(im, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
 
# Show keypoints
cv2.imshow("Keypoints", im_with_keypoints)
cv2.waitKey(0)