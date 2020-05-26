import zipfile
import os
from PIL import Image
import shutil


# TODOs
# Only reduce size, not increase
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


#Checks equality between x and y allowing for some tolerance (t between 0 & 1, relative to y)
def IsEqualWithRelTol(x , y , t):
    return (y*(1-t) <= x)  or  (x <= y*(1+t))


#Original comic will have many pages with the same width (or very similar), but also very different pages such as covers, double-pages, credits...
def GetOriginalPageWidth(tempFolder):
    
    widths = []
    widthsCount = []
    
    #With all the images, make a list of different width values and a list of each value's occurrence
    for dirname, subdirs, files in os.walk(tempFolder):
        for filename in files:
            if IsImage(os.path.join(tempFolder,filename)):
                im = Image.open(os.path.join(tempFolder,filename))
                width = im.width
                if (width not in widths):
                    widths.append(width)
                    widthsCount.append(0)
                widthsCount[widths.index(width)] += 1
    print(widths)
    print(widthsCount)

    #Get most common width
    i = widthsCount.index(max(widthsCount))
    return (widths[i])





#If image was PNG, remove Alpha channel so that it can be saved as JPG
def RemoveAlpha(image):
    if image.mode in ("RGBA", "P"): image = image.convert("RGB")
    return(image)


def ResizeSingleImage(imgPath):
    newWidth = 1280
    quality_val = 90

    img = Image.open(imgPath)
    img = RemoveAlpha(img)
    wpercent = (newWidth/float(img.size[0]))
    newHeight = int((float(img.size[1])*float(wpercent)))
    img = img.resize((newWidth,newHeight), Image.ANTIALIAS)
    img.save(imgPath, 'JPEG', quality=quality_val)



def ResizeImagesInFolder(tempFolder):

    for filename in os.listdir(tempFolder):
        if IsImage(filename):
            imgPath = os.path.join(tempFolder, filename)
            ResizeSingleImage(imgPath)
           
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
print(GetOriginalPageWidth(tempFolder))
ResizeImagesInFolder(tempFolder)


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



