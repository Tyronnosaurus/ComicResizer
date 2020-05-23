import zipfile
import os
from PIL import Image


#--- FUNCTIONS --------------------------
def AddSuffix(filepath):
    return (os.path.splitext(path_to_zip_file)[0]) + ".2.zip"


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
   
    filepath = os.path.join(tempFolder, filename)
    img = Image.open(filepath)
    wpercent = (basewidth/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    img = img.resize((basewidth,hsize), Image.ANTIALIAS)
    img.save(filepath, 'JPEG', quality=quality_val)



#Change format if necessary


#Compress
newFilepath = AddSuffix(path_to_zip_file)
zf = zipfile.ZipFile(newFilepath, "w")
for dirname, subdirs, files in os.walk(tempFolder):
    zf.write(dirname)
    for filename in files:
        zf.write(os.path.join(dirname, filename))
zf.close()


#Delete temp directory

#Rename/delete original file

#Rename new file with original filename



