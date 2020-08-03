import os
import sys
import tkinter as tk
from tkinter import filedialog



#When executing from a file/folder's context menu, sys.arg returns a list of the arguments.
def GetArgument():
    if(len(sys.argv)==2):
        return(sys.argv[1])  #Started from a context menu -> Returns list: [0] is the application's path
                             #                                             [1] is the file/folder's path 
    else:
        return('')           #Started application directly -> No arguments



#Open dialog to select file and put it in the path field
def OpenFileDialog(pathTextBox):
    desktopPath = os.path.expanduser('~') + "/desktop"
    filePath = tk.filedialog.askopenfilename( initialdir=desktopPath , title="Select file" , filetypes=( ("Zip files","*.zip") , ("All files","*.*") ) )
    pathTextBox.delete(0, tk.END)
    pathTextBox.insert(0, filePath)



def cleanPath(path):
    #In Windows, Alt+RightClick on a file lets the user "Copy as path". This string contains two quotemarks,
    # which we remove automatically so that the user doesn't have to do it manually
    if (path[0] == '"'):
        path = path[1:]

    if (path[-1] == '"'):
        path = path[:-1]

    return (path)

#Returns True if file is zip/rar
def IsArchive(path):
    ext = (os.path.splitext(path)[1])
    return (ext in ['.zip', '.rar', '.cbz', '.cbr'])


def IsFolder(path):
    return(os.path.isdir(path))


def IsImage(filename):
    imgExtensions = [".jpg" , ".jpeg" , ".png" , ".bmp"]
    extension = (os.path.splitext(filename)[1])
    return (extension in imgExtensions)


#Checks if x equals y or is relatively close (tolerance between 0 & 1, relative to y)
def IsEqualOrClose(x , y , t):
    return (y*(1-t) <= x)  &  (x <= y*(1+t))