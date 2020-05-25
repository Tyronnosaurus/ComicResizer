import zipfile
import os
from PIL import Image
import shutil


# TODOs
# Implement GIFs
# Implement covers
# Implement GUI or shell integration
# Implement standalone images, not only zips
# Rar support


#--- FUNCTIONS --------------------------
def IsImage(filename):
    imgExtensions = [".jpg" , ".jpeg" , ".png" , ".bmp"]
    extension = (os.path.splitext(filename)[1])
    return (extension in imgExtensions)


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
basewidth = 1280
quality_val = 90

for filename in os.listdir(tempFolder):
    if IsImage(filename):
        filepath = os.path.join(tempFolder, filename)
        img = Image.open(filepath)
        wpercent = (basewidth/float(img.size[0]))
        hsize = int((float(img.size[1])*float(wpercent)))
        img = img.resize((basewidth,hsize), Image.ANTIALIAS)
        img.save(filepath, 'JPEG', quality=quality_val)



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



