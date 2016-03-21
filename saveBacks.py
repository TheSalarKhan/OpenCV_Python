import cv2
import numpy as np
 
c = cv2.VideoCapture(0)
_,f = c.read()


 
avg1 = np.float32(f)
avg2 = np.float32(f)
 
while(1):
    _,f = c.read()

    # f = cv2.cvtColor(f,cv2.COLOR_BGR2GRAY)
     
    cv2.accumulateWeighted(f,avg1,0.1)
    cv2.accumulateWeighted(f,avg2,0.01)
     
    res1 = cv2.convertScaleAbs(avg1)
    res2 = cv2.convertScaleAbs(avg2)


    
 
    cv2.imshow('img',f)
    cv2.imshow('avg1',res1)
    cv2.imshow('avg2',res2)
    k = cv2.waitKey(20) & 0xFF
 
    if k == ord('q'):
        cv2.imwrite('avg1.png',res1)
        cv2.imwrite('avg2.png',res2)
        cv2.imwrite('frame.png',f)
        break
 
cv2.destroyAllWindows()
c.release()
