
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
    tempFolder = (os.path.splitext(filePath)[0]) #Same name as filePath but without extension

    if (Misc.IsArchive(filePath)):
        #For zip and rar files, we extract contents to a temp folder, resize them, and compress them back
        Compression.Extract(filePath, tempFolder)
        ResizeImagesInFolder(tempFolder, newWidth, settings)
        CompressFolderContents(filePath, tempFolder, settings)

    elif (Misc.IsFolder(filePath)):
        #For folders, resize all images inside
        ResizeImagesInFolder(filePath, newWidth, settings.smartResize.get(), settings.onlyReduce.get())


    if (settings.closeWhenFinished.get()):
        import sys
        sys.exit(0)




def ExtractAndPreview(filePath, settings):
    filePath = Misc.cleanPath(filePath)
    tempFolder = (os.path.splitext(filePath)[0]) #Same name as filePath but without extension

    if (Misc.IsArchive(filePath)):
        #For zip and rar files, we extract contents to a temp folder, resize them, and compress them back
        Compression.Extract(filePath, tempFolder)
        os.startfile(tempFolder)
        print("Previewing...", end =" ")
    else:
        print('Not a compressed file')



def ResizeAndCompress(filePath, newWidth, settings):
    filePath = Misc.cleanPath(filePath)
    tempFolder = (os.path.splitext(filePath)[0]) #Same name as filePath but without extension
    
    if (Misc.IsArchive(filePath)):
        ResizeImagesInFolder(tempFolder, newWidth, settings)
        CompressFolderContents(filePath, tempFolder, settings)

    else:
        print('Not a compressed file')








def ResizeImagesInFolder(folderPath, newWidth, settings):
    Resizer.ResizeImagesInFolder(folderPath, newWidth, settings.smartResize.get(), settings.onlyReduce.get())


def CompressFolderContents(filePath, tempFolder, settings):
    if (settings.deleteOriginal.get()):
        send2trash(filePath)    #Delete original file

    Compression.Zip(tempFolder , filePath)

    if (settings.deleteTemp.get()):
        shutil.rmtree(tempFolder)  #Delete temp directory