import cv2
import numpy as np
import urllib
import imutils
import pyautogui
# Sets up the webcam and connects to it and initalizes a variable we use for it
stream = urllib.urlopen('http://192.168.43.1:8080/video')
bytes=b''
heightt  = pyautogui.size()[1]
widthh   = pyautogui.size()[0]

blank_image = np.zeros((heightt,widthh,3), np.uint8)
blank_image[:,:] = (0,255,0)
while True:
    # Takes frames from the camera that we can use
    bytes+=stream.read(16384)
    a = bytes.find(b'\xff\xd8')
    b = bytes.find(b'\xff\xd9')
    if a!=-1 and b!=-1:
        jpg = bytes[a:b+2]
        bytes= bytes[b+2:]
        frame = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.IMREAD_COLOR)
        resized = imutils.resize(frame, 300,200)
       # Displays the final product
        cv2.imshow('frame',blank_image)

     # Hit esc to kill
        if cv2.waitKey(1) ==27:
            exit(0)
