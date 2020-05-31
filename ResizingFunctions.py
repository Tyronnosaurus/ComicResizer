import os
from PIL import Image


#Original comic will have many pages with the same pixel width (or very similar), but also very different pages such as covers, double-pages, credits...
#This function finds the most common width
def GetMostCommonWidth(tempFolder):
    widthsCount = {}    #Dictionary storing pairs of (pixelWidht : ammountOfPagesFound)
    for filename in os.listdir(tempFolder):
        if IsImage(os.path.join(tempFolder,filename)):
            img = Image.open(os.path.join(tempFolder,filename))
            if (img.width not in widthsCount):  #If width not yet in dictionary, add it with ammount 0
                widthsCount[img.width] = 0
            widthsCount[img.width] += 1
    #Return most common width
    return(max(widthsCount))



def IsImage(filename):
    imgExtensions = [".jpg" , ".jpeg" , ".png" , ".bmp"]
    extension = (os.path.splitext(filename)[1])
    return (extension in imgExtensions)
    


#Remove Alpha channel (transparency layer in PNG) so that it can be saved as JPG
def RemoveAlpha(image):
    if image.mode in ("RGBA", "P"): image = image.convert("RGB")
    return(image)



#Checks if x equals y or is relatively close (t between 0 & 1, relative to y)
def IsEqualOrClose(x , y , t):
    return (y*(1-t) <= x)  &  (x <= y*(1+t))



def ResizeSingleImage(imgPath , oldPageWidth , newWidth):
    img = Image.open(imgPath)
    img = RemoveAlpha(img)

    #Case 1: this is a normal page with the usual width
    if IsEqualOrClose(img.width , oldPageWidth , 0.02):
        resizeRatio = (newWidth/float(img.width))
        newHeight = int((float(img.height)*float(resizeRatio)))
    #Case 2: this is a double-page, a crop, or any other size related exception -> 
    else:
        resizeRatio = newWidth / oldPageWidth
        newWidth  = int((float(img.width) *float(resizeRatio)))
        newHeight = int((float(img.height)*float(resizeRatio)))

    if (newWidth >= img.width): return 0  #Do not increase size, only reduce

    img = img.resize((newWidth,newHeight), Image.ANTIALIAS)
    img.save(imgPath, 'JPEG', quality=90)   #75 is low, 95 is highest


#Resize images in folder
def ResizeImagesInSingleFolder(folderPath, newWidth):

    oldWidth = GetMostCommonWidth(folderPath)
  
    for filename in os.listdir(folderPath):
        if IsImage(filename):
            imgPath = os.path.join(folderPath, filename)
            print("Resizing" + imgPath)
            ResizeSingleImage(imgPath , oldWidth , newWidth)



#Resize images in folder (and subfolders, treating each as a different comic)
def ResizeImagesInFolder(topFolder, newWidth):
    for folderName, subfolders, filenames in os.walk(topFolder):
        ResizeImagesInSingleFolder(folderName, newWidth)  #Process each folder inside the directory structure as a single comic