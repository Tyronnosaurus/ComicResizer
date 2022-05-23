import os
from PIL import Image
from Misc import IsEqualOrClose, IsImage, AddFileExistsIndex, GetTempFolder
import Compression
from send2trash import send2trash   #pip install Send2Trash
import shutil

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
    if (image.mode in ("RGBA", "P", "LA")):
        image = image.convert("RGB")
    return(image)



def GetNewDimensions(img, oldMostCommonWidth, newWidth, settings, partOfAComic):
    '''Calculate new dimensions.
        - Smart resizing On:  Detect if this image is noticeably bigger or smaller than the most common width. For these, resize 
                              keeping the old proportion with other pages. Only usable if image is part of a comic (otherwise there
                              would be no oldMostCommonWidth)
        - Smart resizing Off: Normal (dumb) resizing. Just use specified width, and calculate the height by applying the same ratio. '''

    if (settings.smartResize.get() and partOfAComic):
        #Case 1: this is a normally sized page (with 2% tolerance, some scanned pages have a few pixels off)
        if (IsEqualOrClose(img.width , oldMostCommonWidth , 0.02)):
            resizeRatio = (newWidth/float(img.width))
            newHeight = int((float(img.height)*float(resizeRatio)))
        #Case 2: this is a double-page, a crop, or any other size related exception
        else:
            resizeRatio = newWidth / oldMostCommonWidth
            newWidth  = int((float(img.width) *float(resizeRatio)))
            newHeight = int((float(img.height)*float(resizeRatio)))
    else:
        #Case 2: dumb resizing, always resize to width specified by user
        resizeRatio = (newWidth/float(img.width))
        newHeight = int((float(img.height)*float(resizeRatio)))

    return(newWidth,newHeight)




def ResizeArchive(filePath, newWidth, settings):
    tempFolder = GetTempFolder(filePath)

    Compression.Extract(filePath, tempFolder)
    ResizeImagesInFolder(tempFolder, newWidth, settings)
    Compression.Zip(tempFolder, filePath+'.temp')
    
    if (settings.deleteTemp.get()): shutil.rmtree(tempFolder)   #Delete temp directory (if option selected)

    if (os.path.getsize(filePath+'.temp') > os.path.getsize(filePath)):
        send2trash(filePath+'.temp')                                        #If resulting compressed file is larger, keep original
    else:
        if (settings.deleteOriginal.get()): send2trash(filePath)            #Send original file to trash (if option selected)
        os.rename(filePath+'.temp' , AddFileExistsIndex(filePath))




def ResizeSingleImage(imgPath, oldMostCommonWidth, newWidth, settings, partOfAComic):
    with Image.open(imgPath) as img:
        img = RemoveAlpha(img)
        hasChanged = False

        (newWidth,newHeight) = GetNewDimensions(img, oldMostCommonWidth, newWidth, settings, partOfAComic)

        #Apply changes
        if (not (settings.onlyReduce.get() and newWidth>=img.width)):      #Do not increase size, only reduce
            img = img.resize((newWidth,newHeight), Image.ANTIALIAS)
            hasChanged = True

        if ((os.path.splitext(imgPath)[1]) != '.jpg'):      #Check if format has to be changed
            hasChanged = True


        #Resave image (only if it is necessary)
        if (hasChanged):
            newImgPath = (os.path.splitext(imgPath)[0]) + '.jpg'  #Prepare new filename
            img.save(newImgPath, 'JPEG', quality=90)   #75 is low quality, 95 is highest

            #Delete original image (if necessary)
            if (imgPath != newImgPath):     #If resized image keeps the same extension, do not delete original. It has been replaced already and we would delete the resized image
                #Case 1: It's part of a comic, and inside of a temp folder. Delete it always or it will get included in the contents of the zip
                #Case 2: 'Delete Original' checkbox selected. Also delete always, even if it is a standalone image (not part of a comic)
                if (partOfAComic or settings.deleteOriginal.get()):
                    os.remove(imgPath)
                


#Resizes images in a list of images
def ResizeImageList(imageList , newWidth, settings):

    oldWidth = GetMostCommonWidth(imageList)
    
    for imgFile in imageList:
        if IsImage(imgFile):
            ResizeSingleImage(imgFile , oldWidth , newWidth, settings, partOfAComic=True)



#Given a list of filenames, attaches their full path:  hello.txt --> C://Folder//hello.txt
def AttachPathToFilenameList(folderName, filenames):
    filePaths = []
    for filename in filenames:
        filePaths.append(os.path.join(folderName, filename))
    return(filePaths)



#Resize images in folder (and subfolders, treating each as a different comic).
#This is because some times comics come in different folders inside the same archive (e.g. chapters inside a volume, with chapters having different resolutions)
def ResizeImagesInFolder(topFolder, newWidth, settings):
    print("Resizing...", end =" ", flush=True)
    for folderName, _ , filenames in os.walk(topFolder):  #Traverse whole tree. In each folder, we get a list of filenames. The '_' holds list of subdirectories, which is unused

        filePaths = AttachPathToFilenameList(folderName, filenames) #The list of files must contain full paths, not just filenames

        ResizeImageList(filePaths, newWidth, settings)  #Inside each folder, make a list of files and process it

