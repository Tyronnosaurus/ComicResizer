import zipfile
import os
import shutil
from ResizingFunctions import *

# TODOs
# Only reduce size, not increase
# Implement GIFs
# Implement covers
# Implement GUI or shell integration
# Implement standalone images, not only zips
# Rar support


#--- FUNCTIONS --------------------------



#If the file already exists, adds a " (2)" suffix, or higher
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


def Extract(oldFilePath , tempFolder):
    zip_ref = zipfile.ZipFile(oldFilepath, 'r')
    zip_ref.extractall(tempFolder)
    zip_ref.close()


#Checks equality between x and y allowing for some tolerance (t between 0 & 1, relative to y)
def IsEqualWithRelTol(x , y , t):
    return (y*(1-t) <= x)  or  (x <= y*(1+t))



           
#----------------------------------------




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
newFilepath = AddFileExistsIndex(oldFilepath)
zf = zipfile.ZipFile(newFilepath, "w")
for dirname, subdirs, files in os.walk(tempFolder):
    zf.write(dirname)
    for filename in files:
        zf.write(os.path.join(dirname, filename))
zf.close()


######################################################
#Delete temp directory
shutil.rmtree(tempFolder)


######################################################
#Rename new file with original filename



