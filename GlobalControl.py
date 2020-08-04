
import os
import Compression
import Resizer
from send2trash import send2trash   #pip install Send2Trash
import shutil
from Misc import CleanPath, GetTempFolder, IsArchive, IsFolder
import tkinter
import sys


'''Controls high level application flow'''


def ResizeComic(filePath, newWidth, settings):
    
    filePath = CleanPath(filePath)
    tempFolder = GetTempFolder(filePath)

    if (IsArchive(filePath)):  #For compressed files, we extract contents to a temp folder, resize them, and compress them back
        Compression.Extract(filePath, tempFolder)
        Resizer.ResizeImagesInFolder(tempFolder, newWidth, settings)
        if (settings.deleteOriginal.get()): send2trash(filePath)    #Delete original file
        Compression.Zip(tempFolder, filePath)
        if (settings.deleteTemp.get()): shutil.rmtree(tempFolder)  #Delete temp directory if necessary

    elif (IsFolder(filePath)): #For folders, just resize all images inside
        Resizer.ResizeImagesInFolder(filePath, newWidth, settings)


    if (settings.closeWhenFinished.get()): sys.exit(0)  #Exit application




def ExtractAndPreview(filePath, settings):
    filePath = CleanPath(filePath)
    tempFolder = GetTempFolder(filePath)

    if (IsArchive(filePath)):
        #For zip and rar files, we extract contents to a temp folder, resize them, and compress them back
        Compression.Extract(filePath, tempFolder)
        os.startfile(tempFolder)
        print("Previewing...", end =" ")
    else:
        print('Not a compressed file')



def ResizeAndCompress(filePath, newWidth, settings):
    filePath = CleanPath(filePath)
    tempFolder = GetTempFolder(filePath)
    
    if (IsArchive(filePath)):
        Resizer.ResizeImagesInFolder(tempFolder, newWidth, settings)
        if (settings.deleteOriginal.get()): send2trash(filePath)    #Delete original file
        Compression.Zip(tempFolder, filePath)
        if (settings.deleteTemp.get()): shutil.rmtree(tempFolder)  #Delete temp directory if necessary

    else:
        print('Not a compressed file')

 