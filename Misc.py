import os
import sys
import tkinter as tk
from tkinter import filedialog



# When executing from a file/folder's context menu, sys.arg returns a list of the arguments.
def GetArgument():
    if(len(sys.argv)==2):
        return(sys.argv[1])  #Started from a context menu -> Returns list: [0] is the application's path
                             #                                             [1] is the file/folder's path 
    else:
        return('')           #Started application directly -> No arguments



# Open dialog to select file and put it in the path field
def OpenFileDialog(pathTextBox):
    desktopPath = os.path.expanduser('~') + "/desktop"
    filePath = tk.filedialog.askopenfilename( initialdir=desktopPath , title="Select file" , filetypes=( ("Zip files","*.zip") , ("All files","*.*") ) )
    pathTextBox.delete(0, tk.END) # Delete any previous contents
    pathTextBox.insert(0, filePath)



# In Windows, Alt+RightClick on a file lets the user "Copy as path". This string contains two
# quotemarks, which we remove automatically so that the user doesn't have to do it manually.
def CleanPath(path):
    if (path == ''): return(path)   #If empty, return immediately or there will be an error accessing path[0]

    if (path[0]  == '"'):  path = path[1:]
    if (path[-1] == '"'):  path = path[:-1]
    return (path)



# Given a compressed file's path, generates a suitable name for a temporal folder in which to extract its files
def GetTempFolder(filePath):
    return(os.path.splitext(filePath)[0]) #Same name as original filename, but without extension



#############################################################################


# Returns True if file is a compressed archive (zip, rar...)
def IsArchive(path):
    ext = (os.path.splitext(path)[1])
    return (ext in ['.zip', '.rar', '.cbz', '.cbr'])


def IsFolder(path):
    return(os.path.isdir(path))


# Returns True if folder contains mostly images. Allow for some non-image files (typical txt or json with info about the comic)
def IsFolderWithImages(path):
    list = os.listdir(path)
    count = sum(map(lambda x : IsImage(x), list))  # Count odd numbers in the list
    return(count > len(list)*0.8)   #At least 80% of files must be images


def IsImage(path):
    imgExtensions = [".jpg" , ".jpeg" , ".png" , ".bmp"]
    extension = (os.path.splitext(path)[1])
    return (extension in imgExtensions)


# Returns True if folder contains archives (zip, rar...) exclusively. No subfolders either.
def IsFolderWithArchives(path):
    return( all(IsArchive(x) for x in os.listdir(path)) )


#############################################################################



# Checks if x equals y or is relatively close (tolerance between 0 & 1, relative to y)
def IsEqualOrClose(x , y , t):
    return (y*(1-t) <= x)  &  (x <= y*(1+t))



# If the file already exists, adds a " (2)" suffix, or higher
def AddFileExistsIndex(filepath): 
    if not(os.path.exists(filepath)):
        return(filepath)
    else:
        i = 2
        filepathWithoutExt = os.path.splitext(filepath)[0]
        extension          = os.path.splitext(filepath)[1]

        newFilepath = filepathWithoutExt + " (%s)" % i + extension
        while os.path.exists(newFilepath):
            i+=1
            newFilepath = filepathWithoutExt + " (%s)" % i + extension
        return(newFilepath)