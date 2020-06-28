
import os
import shutil
import Resizer
import Compression
from send2trash import send2trash   #pip install Send2Trash
import tkinter






def ResizeComic(filePath, newWidth, deleteOriginal, deleteTemp, smartResize):
    
    print("Working...")

    #Prepare temp folder
    tempFolder = (os.path.splitext(filePath)[0]) #Same name as filePath but without extension
    Compression.Extract(filePath , tempFolder)

    Resizer.ResizeImagesInFolder(tempFolder , newWidth, smartResize)

    #os.startfile(tempFolder)
    #input('press enter')

    if (deleteOriginal):
        send2trash(filePath)    #Delete original file

    Compression.Zip(tempFolder , filePath)

    if (deleteTemp):
        shutil.rmtree(tempFolder)  #Delete temp directory
    
    print("Done")


def SelectFolder():
    from tkinter import filedialog
    desktopPath = os.path.expanduser('~') + "/desktop"
    filePath = tkinter.filedialog.askopenfilename( initialdir=desktopPath , title="Select file" , filetypes=( ("Zip files","*.zip") , ("All files","*.*") ) )
    pathTextBox.delete(0, tkinter.END)
    pathTextBox.insert(0, filePath)





window = tkinter.Tk()
window.geometry("400x300")
window.title("Comic Resizer")

label = tkinter.Label(window, text="Source")
label.grid(row=0, column=0)

pathTextBox = tkinter.Entry(window, width=50)
pathTextBox.grid(row=0, column=1, columnspan=5)

dirDialogButton = tkinter.Button(window, text="...", command=SelectFolder)
dirDialogButton.grid(row=0, column=8)

label = tkinter.Label(window, text="Width")
label.grid(row=1, column=0)

widthTextBox = tkinter.Entry(window, width=5)
widthTextBox.grid(row=1, column=1, sticky='W')
widthTextBox.insert(0, '1280')

label = tkinter.Label(window, text="px")
label.grid(row=1, column=1)

deleteOriginal = tkinter.BooleanVar()
checkBoxDelete = tkinter.Checkbutton(window, text="Delete original", variable=deleteOriginal)
checkBoxDelete.grid(row=3, column=0, columnspan=2, sticky='W', pady=10)

deleteTemp = tkinter.BooleanVar()
checkBoxDeleteTemp = tkinter.Checkbutton(window, text="Delete temp folder", variable=deleteTemp)
checkBoxDeleteTemp.grid(row=3, column=3, columnspan=2, sticky='W')

smartResize = tkinter.BooleanVar()
checkBoxDeleteTemp = tkinter.Checkbutton(window, text="Smart resizing", variable=smartResize)
checkBoxDeleteTemp.grid(row=4, column=0, columnspan=2, sticky='W', pady=10)

buttonResize = tkinter.Button(window, text="Resize", command=lambda:ResizeComic(pathTextBox.get() , int(widthTextBox.get()) , deleteOriginal.get() , deleteTemp.get(), smartResize.get()))
buttonResize.grid(row=5, column=3)


window.mainloop()