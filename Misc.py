import os
import sys



def GetArgument():
    """ When executing from a file/folder's context menu, sys.arg returns a list of the arguments """
    if(len(sys.argv)==2):
        return(sys.argv[1])  #Started from a context menu -> Returns list: [0] is the application's path
                             #                                             [1] is the file/folder's path 
    else:
        return('')           #Started application directly -> No arguments



def CleanPath(path):
    """
    In Windows, Alt+RightClick on a file lets the user "Copy as path". This string contains two
    quotemarks, which we remove automatically so that the user doesn't have to do it manually.
    """
    if (path == ''): return(path)   #If empty, return immediately or there will be an error accessing path[0]

    if (path[0]  == '"'):  path = path[1:]
    if (path[-1] == '"'):  path = path[:-1]
    return (path)



def GetTempFolder(filePath):
    """ Given a compressed file's path, generates a suitable name for a temporal folder in which to extract its files """
    folderName = os.path.splitext(filePath)[0] #Same name as original filename, but without extension
    
    # Windows can't name a folder with trailing periods. If the filename had trailing periods, we have to ignore them.
    # This edge case happens when a comic's title ends with an ellipsis: 'Once upon a time in....zip', for example
    folderName = folderName.rstrip('.')
    
    return(folderName)



#############################################################################


def IsArchive(path):
    """ Returns True if file is a compressed archive (zip, rar...) """
    ext = (os.path.splitext(path)[1])
    return (ext in ['.zip', '.rar', '.cbz', '.cbr'])


def IsFolder(path):
    return(os.path.isdir(path))


def IsFolderWithImages(path):
    """
    Returns True if folder contains mostly images.
    Allow for some non-image files because some times comics have a txt or json with useful info
    """
    list = os.listdir(path)
    count = sum(map(lambda x : IsImage(x), list))  # Count how many of the files are images
    return(count > len(list)*0.8)   #At least 80% of files must be images


def IsImage(path):
    imgExtensions = [".jpg" , ".jpeg" , ".png" , ".bmp"]
    extension = (os.path.splitext(path)[1])
    return (extension in imgExtensions)


def IsFolderWithArchives(path):
    """ Returns True if folder contains archives (zip, rar...) exclusively. No subfolders either. """
    
    return( all(IsArchive(x) for x in os.listdir(path)) )


#############################################################################


def IsEqualOrClose(x , y , t):
    """ Checks if x equals y or is relatively close (tolerance between 0 & 1, relative to y) """
    return (y*(1-t) <= x)  &  (x <= y*(1+t))



def AddFileExistsIndex(filepath):
    """
    Given the filepath of a file we want to create, checks if the file already exists.
    If so, returns the filepath with a " (2)" or higher suffix added: "path/to/file (2).ext"
    """
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