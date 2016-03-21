# import the necessary packages
from imutils.video import WebcamVideoStream
import cv2


vs = WebcamVideoStream(src=0).start()

# loop over some frames...this time using the threaded stream
while True:
	# grab the frame from the threaded video stream and resize it
	# to have a maximum width of 400 pixels
	frame = vs.read()

	cv2.imshow("Frame",frame)
	
	
	key = cv2.waitKey(1) & 0xFF

	if key == ord('q'):
		break

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()
