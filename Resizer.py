import os
from PIL import Image
from Misc import IsEqualOrClose


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
    mostCommonWidth = max(widthsCount, key=widthsCount.get)
    return(mostCommonWidth)




    


#Remove Alpha channel (transparency layer in PNG) so that it can be saved as JPG
def RemoveAlpha(image):
    if image.mode in ("RGBA", "P"): image = image.convert("RGB")
    return(image)



def ResizeSingleImage(imgPath , oldPageWidth , newWidth, smartResize, onlyReduce):
    with Image.open(imgPath) as img:
        img = RemoveAlpha(img)
        hasChanged = False
        
        #Calculate new dimensions
        if (smartResize):
            #Case 1: this is a normal page with the usual width (with 2% tolerance because sometimes pages are a few pixels off)
            if IsEqualOrClose(img.width , oldPageWidth , 0.02):
                resizeRatio = (newWidth/float(img.width))
                newHeight = int((float(img.height)*float(resizeRatio)))
            #Case 2: this is a double-page, a crop, or any other size related exception
            else:
                resizeRatio = newWidth / oldPageWidth
                newWidth  = int((float(img.width) *float(resizeRatio)))
                newHeight = int((float(img.height)*float(resizeRatio)))
        else:
            #Case 2: dumb resizing, always resize to width specified by user
            resizeRatio = (newWidth/float(img.width))
            newHeight = int((float(img.height)*float(resizeRatio)))
    

        #Apply changes
        if not (onlyReduce and newWidth>=img.width):      #Do not increase size, only reduce
            img = img.resize((newWidth,newHeight), Image.ANTIALIAS)
            hasChanged = True

        if ((os.path.splitext(imgPath)[1]) != '.jpg'):    #Check if format has to be changed
            hasChanged = True


        #Resave image only if it is necessary
        if (hasChanged):
            newImgPath = (os.path.splitext(imgPath)[0]) + '.jpg'  #Prepare new filename
            img.save(newImgPath, 'JPEG', quality=90)   #75 is low quality, 95 is highest
        
            if(imgPath != newImgPath):
                os.remove(imgPath) #Delete original
        


#Resizes images in a list of images
def ResizeImageList(imageList , newWidth, smartResize, onlyReduce):

    oldWidth = GetMostCommonWidth(imageList)
    
    for imgFile in imageList:
        if IsImage(imgFile):
            ResizeSingleImage(imgFile , oldWidth , newWidth, smartResize, onlyReduce)



#Given a list of filenames, attaches their full path:  hello.txt --> C://Folder//hello.txt
def AttachPathToFilenameList(folderName, filenames):
    filePaths = []
    for filename in filenames:
        filePaths.append(os.path.join(folderName, filename))
    return(filePaths)



#Resize images in folder (and subfolders, treating each as a different comic).
#This is because some times comics come in different folders inside the same archive (e.g. chapters inside a volume, with chapters having different resolutions)
def ResizeImagesInFolder(topFolder, newWidth, smartResize, onlyReduce):
    for folderName, _ , filenames in os.walk(topFolder):  #Traverse whole tree. In each folder, we get a list of filenames. The '_' holds list of subdirectories, which is unused

        filePaths = AttachPathToFilenameList(folderName, filenames) #The list of files must contain full paths, not just filenames

        ResizeImageList(filePaths, newWidth, smartResize, onlyReduce)  #Inside each folder, make a list of files and process it

