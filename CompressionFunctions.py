import zipfile
import os


def Extract(oldFilePath , tempFolder):
    zip_ref = zipfile.ZipFile(oldFilePath, 'r')
    zip_ref.extractall(tempFolder)
    zip_ref.close()



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
    newFilepath = AddFileExistsIndex(filePath)
    zf = zipfile.ZipFile(newFilepath, "w")
    for dirname, subdirs, files in os.walk(contentsPath):
        zf.write(dirname)
        for filename in files:
            zf.write(os.path.join(dirname, filename))
    zf.close()