
import os
import shutil
import Resizer
import Compression
from send2trash import send2trash   #pip install Send2Trash
import tkinter
import Misc




def ExtractionPhase(filePath, tempFolder):
    print("Working...")
    
    Compression.Extract(filePath , tempFolder)


def ResizingPhase(tempFolder, newWidth, settings):
    Resizer.ResizeImagesInFolder(tempFolder, newWidth, settings.smartResize.get(), settings.onlyReduce.get())

    #os.startfile(tempFolder)
    #input('press enter')


def CompressionPhase(filePath, tempFolder, settings):
    if (settings.deleteOriginal.get()):
        send2trash(filePath)    #Delete original file

    Compression.Zip(tempFolder , filePath)

    if (settings.deleteTemp.get()):
        shutil.rmtree(tempFolder)  #Delete temp directory
    
    print("Done")



def ResizeComic(filePath, newWidth, settings):

    filePath = Misc.cleanPath(filePath)
    tempFolder = (os.path.splitext(filePath)[0]) #Same name as filePath but without extension

    ExtractionPhase(filePath, tempFolder)

    ResizingPhase(tempFolder, newWidth, settings)

    CompressionPhase(filePath, tempFolder, settings)







def OpenFileDialog():
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

dirDialogButton = tkinter.Button(window, text="...", command=OpenFileDialog)
dirDialogButton.grid(row=0, column=8)

label = tkinter.Label(window, text="Width")
label.grid(row=1, column=0)

widthTextBox = tkinter.Entry(window, width=5)
widthTextBox.grid(row=1, column=1, sticky='W')
widthTextBox.insert(0, '1280')

label = tkinter.Label(window, text="px")
label.grid(row=1, column=1)

class Settings:
    deleteOriginal = tkinter.BooleanVar()
    deleteTemp     = tkinter.BooleanVar()
    smartResize    = tkinter.BooleanVar()
    onlyReduce     = tkinter.BooleanVar()
settings = Settings()

checkBoxDelete = tkinter.Checkbutton(window, text="Delete original", variable=settings.deleteOriginal)
checkBoxDelete.grid(row=3, column=0, columnspan=2, sticky='W', pady=10)

checkBoxDeleteTemp = tkinter.Checkbutton(window, text="Delete temp folder", variable=settings.deleteTemp)
checkBoxDeleteTemp.grid(row=3, column=3, columnspan=2, sticky='W')

checkBoxSmart = tkinter.Checkbutton(window, text="Smart resizing", variable=settings.smartResize)
checkBoxSmart.grid(row=4, column=0, columnspan=2, sticky='W', pady=10)
checkBoxSmart.select()

checkBoxOnlyReduce = tkinter.Checkbutton(window, text="Only reduce, don't increase", variable=settings.onlyReduce)
checkBoxOnlyReduce.grid(row=5, column=0, columnspan=3, sticky='W', pady=10)
checkBoxOnlyReduce.select()

buttonResize = tkinter.Button(window, text="Resize", command=lambda:ResizeComic(pathTextBox.get() , int(widthTextBox.get()) , settings))
buttonResize.grid(row=6, column=3)


window.mainloop()