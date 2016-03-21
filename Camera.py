from imutils.video import WebcamVideoStream
def Camera(source=0):
	return WebcamVideoStream(source).start()
