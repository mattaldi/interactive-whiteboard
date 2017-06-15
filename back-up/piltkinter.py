from Tkinter import *
from PIL import Image
from PIL import ImageTk

root = Tk()
root.geometry('640x480')
canvas = Canvas(root,width=640,height=480)
canvas.pack()
pilImage = Image.open("393binary.gif")
image = ImageTk.PhotoImage(pilImage)
imagesprite = canvas.create_image(0,400,image=image)
root.mainloop()
