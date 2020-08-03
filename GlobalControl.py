
import os
import Compression
import Resizer
from send2trash import send2trash   #pip install Send2Trash
import shutil
import Misc
import tkinter

'''Controls high level application flow'''


def ExtractToTempFolder(filePath):
    tempFolder = (os.path.splitext(filePath)[0]) #Same name as filePath but without extension
    Compression.Extract(filePath , tempFolder)
    return(tempFolder)


def ResizeImagesInFolder(folderPath, newWidth, settings):
    Resizer.ResizeImagesInFolder(folderPath, newWidth, settings.smartResize, settings.onlyReduce)


def CompressFolderContents(filePath, tempFolder, settings):
    if (settings.deleteOriginal):
        send2trash(filePath)    #Delete original file

    Compression.Zip(tempFolder , filePath)

    if (settings.deleteTemp):
        shutil.rmtree(tempFolder)  #Delete temp directory
    
    



def ResizeComic(filePath, newWidth, settings):

    print("Working...")
    
    filePath = Misc.cleanPath(filePath)


    if (Misc.IsArchive(filePath)):
        #For zip and rar files, we extract contents to a temp folder, resize them, and compress them back
        tempFolder = ExtractToTempFolder(filePath)
        ResizeImagesInFolder(tempFolder, newWidth, settings)
        CompressFolderContents(filePath, tempFolder, settings)

    elif (Misc.IsFolder(filePath)):
        #For folders, resize all images inside
        ResizeImagesInFolder(filePath, newWidth, settings.smartResize, settings.onlyReduce)


    print("Done")