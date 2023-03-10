import os

def findPath(filename):
    cwd=os.getcwd()
    print(cwd)
    filepath=os.path.abspath(os.path.join(cwd, filename))
    return filepath

import tkinter as tk
from PIL import Image, ImageTk

def resize(img,height,width):
    img=Image.open(findPath(f"material/picture/{img}"))

    if height==0:
        height=width*(img.height/img.width)
        height=int(height)
    
    elif width==0:
        width=height*(img.width/img.height)
        width=int(width)

    return img.resize((width,height))

# NSCbannerImg=resize()



root=tk.Tk()
root.iconbitmap(findPath("material/picture/motor.ico"))
# NSCbanner=ImageTk.PhotoImage(Image.open(r"material\picture\NSCboard.jpg"))
NSCbanner=ImageTk.PhotoImage(resize("NSCbanner.jpg",300,1520))
tk.Label(image=NSCbanner).pack(side='top',expand=True)

root.mainloop()

print(findPath("material/picture"))