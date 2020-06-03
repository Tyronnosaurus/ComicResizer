
import os
import shutil
import Resizer
import Compression
from send2trash import send2trash   #pip install Send2Trash


print("Working...")

oldFilepath = r'C:\Users\Eduard\Desktop\AAA.zip'

#Prepare temp folder name (it's just the filepath with the extension removed)
tempFolder = (os.path.splitext(oldFilepath)[0])


Compression.Extract(oldFilepath , tempFolder)


newWidth = 1280
Resizer.ResizeImagesInFolder(tempFolder , newWidth)

os.startfile(tempFolder)
input('press enter')

#send2trash(oldFilepath)    #Delete original file


Compression.Zip(tempFolder , oldFilepath)


#shutil.rmtree(tempFolder)  #Delete temp directory



