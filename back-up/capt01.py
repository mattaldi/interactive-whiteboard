import numpy as np
import cv2

cap = cv2.VideoCapture('output-04.avi')
cap.set(3,120)
cap.set(4,102)
while(cap.isOpened()):
    try:
        ret, frame = cap.read()
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    except:
        cap = cv2.VideoCapture('output-04.avi')



