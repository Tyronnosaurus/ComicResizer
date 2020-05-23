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

def AddSuffix(filepath):
    return (os.path.splitext(filepath)[0]) + ".2.zip"

#----------------------------------------



print("Working...")

path_to_zip_file = 'C:\\Users\\Eduard\\Desktop\\AAA.zip'


#Prepare temp folder name (it's just the filepath with the extension removed)
tempFolder = (os.path.splitext(path_to_zip_file)[0])


#Extract
zip_ref = zipfile.ZipFile(path_to_zip_file, 'r')
zip_ref.extractall(tempFolder)
zip_ref.close()



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



#Compress
newFilepath = AddSuffix(path_to_zip_file)
zf = zipfile.ZipFile(newFilepath, "w")
for dirname, subdirs, files in os.walk(tempFolder):
    zf.write(dirname)
    for filename in files:
        zf.write(os.path.join(dirname, filename))
zf.close()



#Delete temp directory
shutil.rmtree(tempFolder)



#Rename/delete original file

#Rename new file with original filename



