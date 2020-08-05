import os
import Compression
import Resizer
from send2trash import send2trash   #pip install Send2Trash
import shutil
from Misc import CleanPath, GetTempFolder, IsArchive, IsFolder
import sys
import tkinter.messagebox


'''------------------------------------'''
'''Controls high level application flow'''
'''------------------------------------'''

#User pressed 'Resize' button: do the whole process (extract, resize, compress)
def ResizeComic(filePath, newWidth, settings):
    
    filePath = CleanPath(filePath)
    tempFolder = GetTempFolder(filePath)

    if (IsArchive(filePath)):  #For compressed files, we extract contents to a temp folder, resize them, and compress them back
        Compression.Extract(filePath, tempFolder)
        Resizer.ResizeImagesInFolder(tempFolder, newWidth, settings)
        if (settings.deleteOriginal.get()): send2trash(filePath)    #Send original file to trash (if option selected)
        Compression.Zip(tempFolder, filePath)
        if (settings.deleteTemp.get()): shutil.rmtree(tempFolder)   #Delete temp directory (if option selected)

    elif (IsFolder(filePath)): #For folders, just resize all images inside
        Resizer.ResizeImagesInFolder(filePath, newWidth, settings)

    if (settings.closeWhenFinished.get()): sys.exit(0)  #Exit application (if option selected)




## User can use the 2 small 'Substep' buttons to do the resizing in two phases and preview images before resizing
## (and delete or edit any image if desired). Only useful for compressed files, not folders or imagelists.
#Step 1: Extract to temp folder and show this folder in explorer
def ExtractAndPreview(filePath, settings):
    filePath = CleanPath(filePath)
    tempFolder = GetTempFolder(filePath)

    if (IsArchive(filePath)):
        Compression.Extract(filePath, tempFolder)
        os.startfile(tempFolder)
        print("Previewing...", end =" ", flush=True)
    else:
        tkinter.messagebox.showinfo(title='Nothing to extract', message='Selected source is not a compressed file, so no extraction will be done.')


#Step 2: Do the rest of the operations
def ResizeAndCompress(filePath, newWidth, settings):
    filePath = CleanPath(filePath)
    tempFolder = GetTempFolder(filePath)
    
    if (IsArchive(filePath)):
        Resizer.ResizeImagesInFolder(tempFolder, newWidth, settings)
        if (settings.deleteOriginal.get()): send2trash(filePath)    #Send original file to trash (if option selected)
        Compression.Zip(tempFolder, filePath)
        if (settings.deleteTemp.get()): shutil.rmtree(tempFolder)   #Delete temp directory (if option selected)

    if (settings.closeWhenFinished.get()): sys.exit(0)  #Exit application (if option selected)
 