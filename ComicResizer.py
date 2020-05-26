
import os
import shutil
from ResizingFunctions import ResizeImagesInFolder
from CompressionFunctions import *

# TODOs
# Only reduce size, not increase
# Implement GIFs
# Implement GUI or shell integration
# Implement standalone images, not only zips
# Rar support
# If all files inside a root folder, move them to root



print("Working...")

oldFilepath = 'C:\\Users\\Eduard\\Desktop\\AAA.zip'

######################################################
#Prepare temp folder name (it's just the filepath with the extension removed)
tempFolder = (os.path.splitext(oldFilepath)[0])

######################################################
#Extract
Extract(oldFilepath , tempFolder)


######################################################
#Resize
newWidth = 1280
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



