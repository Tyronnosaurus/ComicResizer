
import os
import shutil
import Resizer
import Compression
from send2trash import send2trash   #pip install Send2Trash
import tkinter






def ResizeComic(filePath, newWidth):
    
    print("Working...")

    #Prepare temp folder 
    tempFolder = (os.path.splitext(filePath)[0]) #Same name as filePath but without extension
    Compression.Extract(filePath , tempFolder)

    Resizer.ResizeImagesInFolder(tempFolder , newWidth)

    #os.startfile(tempFolder)
    #input('press enter')

    #send2trash(filePath)    #Delete original file

    Compression.Zip(tempFolder , filePath)

    #shutil.rmtree(tempFolder)  #Delete temp directory




#filePath = r'C:\Users\Eduard\Desktop\AAA.zip'



window = tkinter.Tk()
window.geometry("400x300")
window.title("Comic Resizer")

label = tkinter.Label(window, text="Source")
label.pack()

pathTextBox = tkinter.Entry(window, width=50)
pathTextBox.pack()

label = tkinter.Label(window, text="Width")
label.pack()

widthTextBox = tkinter.Entry(window, width=5)
widthTextBox.pack()

label = tkinter.Label(window, text="px")
label.pack()

pathTextBox.insert(0, r'C:\Users\Eduard\Desktop\AAA.zip')
widthTextBox.insert(0, '1280')

newWidth = int(widthTextBox.get())
filePath = pathTextBox.get()

button1 = tkinter.Button(window, text="Resize", command=lambda:ResizeComic(filePath,newWidth))
button1.pack()

window.mainloop()