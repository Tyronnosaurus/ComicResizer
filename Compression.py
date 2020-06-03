import zipfile
import rarfile
import os



def Unzip(filePath , destinationPath):
    zf = zipfile.ZipFile(filePath, 'r')
    zf.extractall(destinationPath)
    zf.close()

def Unrar(filePath , destinationPath):
    rf = rarfile.RarFile(filePath, 'r')
    rf.extractall(destinationPath)
    rf.close()

def Extract(filePath , destinationPath):
    ext = (os.path.splitext(filePath)[1])
    if (ext == '.zip'):
        Unzip(filePath , destinationPath)
    elif (ext == '.rar'):
        Unrar(filePath , destinationPath)



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



def Zip(contentsPath , filePath):

    newFilePath = filePath.replace('.rar','.zip')
    newFilepath = AddFileExistsIndex(newFilePath)


    zf = zipfile.ZipFile(newFilepath, "w")
    for folderName, _, filenames in os.walk(contentsPath):
       for filename in filenames:
           filePath = os.path.join(folderName, filename)    #Create complete filepath of file in directory
           zf.write(filePath)   #Add file to zip
    zf.close()