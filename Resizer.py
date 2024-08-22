import os
from PIL import Image
from Misc import IsEqualOrClose, IsImage, IsArchive, AddFileExistsIndex, GetTempFolder
import Compression
from send2trash import send2trash   #pip install Send2Trash
import shutil


''' High level functions for resizing comics in different presentations (archive, folder with images, single image, folder with archives for batch resizing...) '''

# If the comic is inside a compressed file (zip, rar....), we must temporarily extract it
def ResizeArchive(filePath, newWidth, settings):
    ## Extract to a temp folder
    tempFolder = GetTempFolder(filePath)
    Compression.Extract(filePath, tempFolder)

    # Resize all images inside, folder by folder
    ResizeFolderRecursively(tempFolder, newWidth, settings)
    
    # Compress back
    # Add a '.temp' suffix because the original still exists (we still don't know which to keep)
    Compression.Zip(tempFolder, filePath+'.temp')

    # Decide wheter to keep the original, the resized, or both
    if (os.path.getsize(filePath + '.temp') > os.path.getsize(filePath)):     # If resulting compressed file is larger, keep original
        send2trash(filePath + '.temp')
    else:                                                                   # Otherwise, keep the new resized one. 
        if (settings.deleteOriginal): send2trash(filePath)   # Delete original (if option selected)
        os.rename(filePath + '.temp' , AddFileExistsIndex(filePath)) # Remove '.temp' suffix

    #Delete temp directory (if option selected)
    if (settings.deleteTemp): shutil.rmtree(tempFolder)



# Resizes everything in a folder and subfolders:
# - If folder has images, resizes them (treating all images in each folder as one comic)
# - If folder has archives, resizes them
# - If folder has subfolders, repeats the process recursively
# A folder can have more than one of the previous items mixed in.
def ResizeFolderRecursively(topFolder, newWidth, settings):
    print("Resizing folder: " + topFolder)
    for folderName, _ , filenames in os.walk(topFolder):
        # Resize images in current folder
        filePaths = [x for x in filenames if IsImage(x)]
        if (len(filePaths)>0):
            filePaths = AttachPathToFilenameList(folderName, filenames) # The list of files must contain full paths, not just filenames
            ResizeImageList(filePaths, newWidth, settings)              # Inside each folder, make a list of files and process it

        # Resize archives in current folder
        filePaths = [x for x in filenames if IsArchive(x)]
        for file in filePaths:
            file = os.path.join(folderName,file) #Must contain full paths, not just filenames
            ResizeArchive(file)


# Resize images in folder (and subfolders, treating each as a different comic).
# This is because some times comics come in different folders inside the same archive (e.g. chapters inside a volume, with chapters having different resolutions)
def ResizeImagesInFolder(topFolder, newWidth, settings):
    
    print("Resizing...")

    for folderName, _ , filenames in os.walk(topFolder):  # Traverse whole tree. In each folder, we get a list of filenames. The '_' holds list of subdirectories, which is unused
        filePaths = AttachPathToFilenameList(folderName, filenames) # The list of files must contain full paths, not just filenames
        ResizeImageList(filePaths, newWidth, settings)              # Inside each folder, make a list of files and process it




# Resizes images in a list of images
def ResizeImageList(imageList , newWidth, settings):

    oldWidth = GetMostCommonWidth(imageList) if settings.smartResize else 0
    
    for imgFile in imageList:
        if IsImage(imgFile):
            ResizeImageInComic(imgFile , oldWidth , newWidth, settings, partOfAComic=True)




def ResizeImageInComic(imgPath, oldMostCommonWidth, newWidth, settings, partOfAComic):
    with Image.open(imgPath) as img:
        img = RemoveAlpha(img)
        hasChanged = False

        (newWidth,newHeight) = GetNewDimensionsOfPage(img, oldMostCommonWidth, newWidth, settings, partOfAComic)

        # Apply changes
        if (not (settings.onlyReduce and newWidth>=img.width)):      # Option: Do not increase size, only reduce
            img = img.resize((newWidth,newHeight), Image.LANCZOS)
            hasChanged = True

        if ((os.path.splitext(imgPath)[1]) != '.jpg'):      # Check if format has to be changed
            hasChanged = True

        # Resave image (only if it is necessary)
        if (hasChanged):
            newImgPath = (os.path.splitext(imgPath)[0]) + '.jpg'  #Prepare new filename
            img.save(newImgPath, 'JPEG', quality=90)   #75 is low quality, 95 is highest

            # Delete original image (if necessary)
            if (imgPath != newImgPath):     # If resized image keeps the same extension, do not delete original. It has been replaced already and we would delete the resized image
                # Case 1: It's part of a comic, and inside of a temp folder. Delete it always or it will get included in the contents of the zip
                # Case 2: 'Delete Original' checkbox selected. Also delete always, even if it is a standalone image (not part of a comic)
                if (partOfAComic or settings.deleteOriginal):
                    os.remove(imgPath)




# For a standalone image (not part of a comic), don't apply smart resizing
def ResizeSingleImage(imgPath, newWidth, settings):
    ResizeImageInComic(imgPath, 0, newWidth, settings, partOfAComic=False)  # Reuse code





## Smart resizing ########################################################################


# Calculate new dimensions. This is done for every page. Most will get resized to the user-specified goal width, but some will require different scaling rules
def GetNewDimensionsOfPage(img, oldMostCommonWidth, goalWidth, settings, partOfAComic):

    if (settings.smartResize and partOfAComic): return( GetNewDimensionsOfPage_Smart(img, oldMostCommonWidth, goalWidth) )
    else:                                       return( GetNewDimensionsOfPage_Dumb(img, goalWidth) )


#Smart resizing: If a page from a comic is noticeably bigger or smaller than most pages (like a doublespread), resize accordingly.
def GetNewDimensionsOfPage_Smart(img, oldMostCommonWidth, goalWidth):
    
    # Do not resize if it's already the goal size
    if (IsEqualOrClose(img.width , goalWidth , 0.02)):
        (newWidth,newHeight) = (img.width,img.height)

    # Case 1: this is a normally sized page 
    if (PageIsNormallySized(img, oldMostCommonWidth)):
        (newWidth,newHeight) = GetNewDimensionsOfPage_Dumb(img, goalWidth)
    

    # Case 2: larger than most pages. Example: doublepages, wallpapers...
    elif (img.width > oldMostCommonWidth):
        resizeRatio = goalWidth / oldMostCommonWidth
        newWidth  = int((float(img.width) *float(resizeRatio)))
        newHeight = int((float(img.height)*float(resizeRatio)))


    # Case 3: smaller than most pages. Example: croppings, translator's credits at the end...
    else:
        # If it's already smaller than the goal width, do not scale at all (or else we end up with microscopic images)
        if (img.width<=img.width):  (newWidth,newHeight) = (img.width, img.height)
        
        # If it's larger than the goal width, scale down to the goal width, and no more
        else:                       (newWidth,newHeight) = GetNewDimensionsOfPage_Dumb(img, goalWidth)


    return(newWidth,newHeight)




## Auxiliar methods ########################################################################

# Dumb resizing: Just resize every image to the width specified by the user.
def GetNewDimensionsOfPage_Dumb(img, newWidth):
    #Case 2: dumb resizing, always resize to width specified by user
    resizeRatio = (newWidth/float(img.width))
    newHeight = int((float(img.height)*float(resizeRatio)))
    return(newWidth,newHeight)





# Original comic will have many pages with the same pixel width (or very similar), but also very different pages such as covers, double-pages, credits...
# This function finds the most common width
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




# Given a list of filenames, attaches their full path:  hello.txt --> C://Folder//hello.txt
def AttachPathToFilenameList(folderName, filenames):
    filePaths = []
    for filename in filenames:
        filePaths.append(os.path.join(folderName, filename))
    return(filePaths)



#Remove Alpha channel (transparency layer in PNG) so that it can be saved as JPG
def RemoveAlpha(image):
    if (image.mode in ("RGBA", "P", "LA")):
        image = image.convert("RGB")
    return(image)



# Returns True if page is normally sized (has the same dimensions as most other pages)
# (within 2% tolerance because some scanned pages tend to be a few pixels off)
def PageIsNormallySized(img, oldMostCommonWidth):
    return( IsEqualOrClose(img.width , oldMostCommonWidth , 0.02) )
