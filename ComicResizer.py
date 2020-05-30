
import os
import shutil
from ResizingFunctions import ResizeImagesInFolder
from CompressionFunctions import *


print("Working...")

oldFilepath = r'C:\Users\Eduard\Desktop\AAA.zip'

######################################################
#Prepare temp folder name (it's just the filepath with the extension removed)
tempFolder = (os.path.splitext(oldFilepath)[0])

######################################################
#Extract
Extract(oldFilepath , tempFolder)


######################################################
#Resize
newWidth = 400 #1280
ResizeImagesInFolder(tempFolder , newWidth)


######################################################
#Delete original file
from send2trash import send2trash   #pip install Send2Trash
#send2trash(oldFilepath)


######################################################
#Compress
Zip(tempFolder , oldFilepath)


######################################################
#Delete temp directory
#shutil.rmtree(tempFolder)


######################################################
#Rename new file with original filename



