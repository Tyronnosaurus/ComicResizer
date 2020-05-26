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



def ResizeSingleImage(imgPath , oldWidth , newWidth):
    quality_val = 90

    img = Image.open(imgPath)
    img = RemoveAlpha(img)
    wpercent = (newWidth/float(img.size[0]))
    newHeight = int((float(img.size[1])*float(wpercent)))
    img = img.resize((newWidth,newHeight), Image.ANTIALIAS)
    img.save(imgPath, 'JPEG', quality=quality_val)



def ResizeImagesInFolder(tempFolder , newWidth):

    oldWidth = GetBaseWidth(tempFolder)

    for filename in os.listdir(tempFolder):
        if IsImage(filename):
            imgPath = os.path.join(tempFolder, filename)
            ResizeSingleImage(imgPath , oldWidth , newWidth)