import os
import Compression
import Resizer
from Misc import CleanPath, IsArchive, IsFolder, IsImage, GetTempFolder
import sys
import tkinter.messagebox
from send2trash import send2trash   #pip install Send2Trash
import shutil

'''------------------------------------'''
'''Controls high level application flow'''
'''------------------------------------'''

#User pressed 'Resize' button: do the whole process (extract, resize, compress)
def ResizeComic(filePath, newWidth, settings):
    
    filePath = CleanPath(filePath)
    

    # For compressed files, we extract contents to a temp folder, resize them as a comic, and compress them back
    if (IsArchive(filePath)):   Resizer.ResizeArchive(filePath, newWidth, settings)

    # For a folder, resize everything in it and its subfolders recursively
    elif (IsFolder(filePath)):  Resizer.ResizeFolderRecursively(filePath, newWidth, settings)

    # For a standalone image, just resize it
    elif (IsImage(filePath)):   Resizer.ResizeSingleImage(filePath, newWidth, settings)

    # For everything else, show an error listing which files are valid
    else:                       ShowInvalidSourceError()
        

    if (settings.closeWhenFinished.get()): sys.exit(0)  #Exit application (if option selected)




# Show an error popup listing which files are valid
def ShowInvalidSourceError():
    tkinter.messagebox.showinfo(title='Source not valid',
                                message='Valid files are:\n Archives (zip, rar, cbz, cbr)\n Folders\n Single images')
       


## User can use the 2 small 'Substep' buttons to do the resizing in two phases and preview images before resizing
## (and delete or edit any image if desired). Only useful for compressed files, not folders or imagelists.

#Substep 1: Extract to temp folder and show this folder in explorer
def ExtractAndPreview(filePath, settings):
    filePath = CleanPath(filePath)
    tempFolder = GetTempFolder(filePath)

    if (IsArchive(filePath)):
        Compression.Extract(filePath, tempFolder)
        os.startfile(tempFolder)
        print("Previewing...", end =" ", flush=True)
    else:
        tkinter.messagebox.showinfo(title='Nothing to extract', message='Selected source is not a compressed file, so no extraction will be done.')


#Substep 2: Do the rest of the operations
def ResizeAndCompress(filePath, newWidth, settings):
    filePath = CleanPath(filePath)
    tempFolder = GetTempFolder(filePath)
    
    if (IsArchive(filePath)):
        Resizer.ResizeImagesInFolder(tempFolder, newWidth, settings)
        if (settings.deleteOriginal.get()): send2trash(filePath)    #Send original file to trash (if option selected)
        Compression.Zip(tempFolder, filePath)
        if (settings.deleteTemp.get()): shutil.rmtree(tempFolder)   #Delete temp directory (if option selected)

    if (settings.closeWhenFinished.get()): sys.exit(0)  #Exit application (if option selected)
 