import cv2
import numpy as np
import urllib
from Tkinter import *
from PIL import Image
from PIL import ImageTk
import tkFileDialog
import threading

stream = urllib.urlopen('http://192.168.43.1:8080/video')
bytes=b''
root = Tk()
root.geometry('640x480')
canvas = Canvas(root,width=640,height=480)
canvas.pack()

stopEvent = threading.Event()
while True:
    bytes+=stream.read(16384)
    a = bytes.find(b'\xff\xd8')
    b = bytes.find(b'\xff\xd9')
    
    if a!=-1 and b!=-1:
        jpg = bytes[a:b+2]
        bytes= bytes[b+2:]
        frame = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.IMREAD_COLOR)


        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        image = ImageTk.PhotoImage(image)
        imagesprite = canvas.create_image(0,400,image=image)

        

        root.mainloop()


