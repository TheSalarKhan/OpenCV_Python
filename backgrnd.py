import cv2

cam = cv2.VideoCapture(0)

ret, bg = cam.read()

while True:
    ret, frame = cam.read()
    frame = cv2.blur(frame, (5,5))
    mask = cv2.absdiff(frame, bg)

    gray = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    ret, gray = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
    gray = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, kernel)

    gray = cv2.blur(gray, (9,9))
    cv2.imshow("mask", mask)
    cv2.imshow("gray", gray)
    cv2.imshow("webcam", frame)
    
    if cv2.waitKey(2) & 0xFF == 27:
        break

cam.release()
cv2.destroyAllWindows()