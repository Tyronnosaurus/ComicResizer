import os
from PIL import Image



#Original comic will have many pages with the same width (or very similar), but also very different pages such as covers, double-pages, credits...
def GetBaseWidth(tempFolder):
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
    #Get most common width
    i = widthsCount.index(max(widthsCount))
    return (widths[i])




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
    quality_val = 90    #75 is low, 95 is highest

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

    img = img.resize((newWidth,newHeight), Image.ANTIALIAS)
    img.save(imgPath, 'JPEG', quality=quality_val)



def ResizeImagesInFolder(tempFolder , newWidth):

    oldWidth = GetBaseWidth(tempFolder)

    for filename in os.listdir(tempFolder):
        if IsImage(filename):
            imgPath = os.path.join(tempFolder, filename)
            ResizeSingleImage(imgPath , oldWidth , newWidth)