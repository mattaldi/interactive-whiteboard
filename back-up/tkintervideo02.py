#!/usr/bin/python

import numpy as np
from multiprocessing import Process, Queue
from Queue import Empty
import cv2
from PIL import Image, ImageTk
import time
import Tkinter as tk

#tkinter GUI functions----------------------------------------------------------
def quit_(root, process):
   process.join()
   root.destroy()

def update_image(image_label, queue):
   frame = queue.get()
   im = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
   a = Image.fromarray(im)
   b = ImageTk.PhotoImage(image=a)
   image_label.configure(image=b)
   image_label._image_cache = b  # avoid garbage collection
   root.update()

def update_all(root, image_label, queue):
   update_image(image_label, queue)
   root.after(0, func=lambda: update_all(root, image_label, queue))

#multiprocessing image processing functions-------------------------------------
def image_capture(queue):
   vidFile = cv2.VideoCapture(0)
   while True:
      try:
         flag, frame=vidFile.read()
         if flag==0:
            break
         queue.put(frame)
         cv2.waitKey(20)
      except:
         continue

if __name__ == '__main__':
   queue = Queue()
   print 'queue initialized...'
   root = tk.Tk()
   print 'GUI initialized...'
   image_label = tk.Label(master=root)# label for the video frame
   image_label.pack()
   print 'GUI image label initialized...'
   p = Process(target=image_capture, args=(queue,))
   p.start()
   print 'image capture process has started...'
   # quit button
   quit_button = tk.Button(master=root, text='Quit',command=lambda: quit_(root,p))
   quit_button.pack()
   print 'quit button initialized...'
   # setup the update callback
   root.after(0, func=lambda: update_all(root, image_label, queue))
   print 'root.after was called...'
   root.mainloop()
   print 'mainloop exit'
   p.join()
   print 'image capture process exit'
