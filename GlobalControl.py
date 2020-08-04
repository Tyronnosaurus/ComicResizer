
import os
import Compression
import Resizer
from send2trash import send2trash   #pip install Send2Trash
import shutil
import Misc
import tkinter

'''Controls high level application flow'''


def ResizeComic(filePath, newWidth, settings):
    
    filePath = Misc.cleanPath(filePath)
    tempFolder = GetTempFolder(filePath)

    if (Misc.IsArchive(filePath)):
        #For zip and rar files, we extract contents to a temp folder, resize them, and compress them back
        Compression.Extract(filePath, tempFolder)
        Resizer.ResizeImagesInFolder(tempFolder, newWidth, settings)
        CompressFolderContents(filePath, tempFolder, settings)

    elif (Misc.IsFolder(filePath)):
        #For folders, resize all images inside
        Resizer.ResizeImagesInFolder(filePath, newWidth, settings)


    if (settings.closeWhenFinished.get()):
        import sys
        sys.exit(0)




def ExtractAndPreview(filePath, settings):
    filePath = Misc.cleanPath(filePath)
    tempFolder = GetTempFolder(filePath)

    if (Misc.IsArchive(filePath)):
        #For zip and rar files, we extract contents to a temp folder, resize them, and compress them back
        Compression.Extract(filePath, tempFolder)
        os.startfile(tempFolder)
        print("Previewing...", end =" ")
    else:
        print('Not a compressed file')



def ResizeAndCompress(filePath, newWidth, settings):
    filePath = Misc.cleanPath(filePath)
    tempFolder = GetTempFolder(filePath)
    
    if (Misc.IsArchive(filePath)):
        Resizer.ResizeImagesInFolder(tempFolder, newWidth, settings)
        CompressFolderContents(filePath, tempFolder, settings)

    else:
        print('Not a compressed file')




def GetTempFolder(filePath):
    return(os.path.splitext(filePath)[0]) #Same name as filePath but without extension


def CompressFolderContents(filePath, tempFolder, settings):
    if (settings.deleteOriginal.get()):
        send2trash(filePath)    #Delete original file

    Compression.Zip(tempFolder , filePath)

    if (settings.deleteTemp.get()):
        shutil.rmtree(tempFolder)  #Delete temp directory