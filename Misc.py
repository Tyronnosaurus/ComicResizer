import os


def cleanPath(path):
    #In Windows, Alt+RightClick on a file lets the user "Copy as path". This string contains two quotemarks,
    # which we remove automatically so that the user doesn't have to do it manually
    if (path[0] == '"'):
        path = path[1:]

    if (path[-1] == '"'):
        path = path[:-1]

    return (path)


def IsArchive(path):
    ext = (os.path.splitext(path)[1])
    return (ext in ['.zip', '.rar'])


def IsFolder(path):
    return(os.path.isdir(path))


#Checks if x equals y or is relatively close (tolerance between 0 & 1, relative to y)
def IsEqualOrClose(x , y , t):
    return (y*(1-t) <= x)  &  (x <= y*(1+t))