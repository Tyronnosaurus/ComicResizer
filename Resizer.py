import os
from PIL import Image


#Original comic will have many pages with the same pixel width (or very similar), but also very different pages such as covers, double-pages, credits...
#This function finds the most common width
def GetMostCommonWidth(imgList):
    widthsCount = {}    #Dictionary storing pairs of (pixelWidht : ammountOfPagesFound)
    for filePath in imgList:
        if IsImage(filePath):
            img = Image.open(filePath)
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

    #Case 1: this is a normal page with the usual width (with 2% tolerance because sometimes pages are a few pixels off)
    if IsEqualOrClose(img.width , oldPageWidth , 0.02):
        resizeRatio = (newWidth/float(img.width))
        newHeight = int((float(img.height)*float(resizeRatio)))
    #Case 2: this is a double-page, a crop, or any other size related exception
    else:
        resizeRatio = newWidth / oldPageWidth
        newWidth  = int((float(img.width) *float(resizeRatio)))
        newHeight = int((float(img.height)*float(resizeRatio)))

    if (newWidth >= img.width): return 0  #Do not increase size, only reduce

    img = img.resize((newWidth,newHeight), Image.ANTIALIAS)

    os.remove(imgPath) #Delete original
    newImgPath = (os.path.splitext(imgPath)[0]) + '.jpg'  #Prepare new filename
    img.save(newImgPath, 'JPEG', quality=90)   #75 is low quality, 95 is highest


#Resize images in folder
def ResizeImagesInSingleFolder(folderPath, newWidth):

    oldWidth = GetMostCommonWidth(folderPath)
  
    for filename in os.listdir(folderPath):
        if IsImage(filename):
            imgPath = os.path.join(folderPath, filename)
            ResizeSingleImage(imgPath , oldWidth , newWidth)


#Resizes images in a list of images
def ResizeImageList(imageList , newWidth):

    oldWidth = GetMostCommonWidth(imageList)
    
    for imgFile in imageList:
        if IsImage(imgFile):
            ResizeSingleImage(imgFile , oldWidth , newWidth)



#Given a list of filenames, attaches their full path:  hello.txt --> C://Folder//hello.txt
def AttachPathToFilenameList(folderName, filenames):
    filePaths = []
    for filename in filenames:
        filePaths.append(os.path.join(folderName, filename))
    return(filePaths)



#Resize images in folder (and subfolders, treating each as a different comic).
#This is because some times comics come in different folders inside the same archive (e.g. chapters inside a volume, with chapters having different resolutions)
def ResizeImagesInFolder(topFolder, newWidth):
    for folderName, _ , filenames in os.walk(topFolder):  #Traverse whole tree. In each folder, we get a list of filenames. The '_' holds list of subdirectories, which is unused

        filePaths = AttachPathToFilenameList(folderName, filenames) #The list of files must contain full paths, not just filenames

        ResizeImageList(filePaths, newWidth)  #Inside each folder, make a list of files and process it

