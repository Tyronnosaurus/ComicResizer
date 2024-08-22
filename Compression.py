import zipfile
import rarfile
import os
from Misc import AddFileExistsIndex



def Unzip(filePath , destinationPath):
    zf = zipfile.ZipFile(filePath, 'r')
    zf.extractall(destinationPath)
    zf.close()

def Unrar(filePath , destinationPath):
    rf = rarfile.RarFile(filePath, 'r')
    rf.extractall(destinationPath)
    rf.close()

def Extract(filePath , destinationPath):
    print("Extracting...")
    ext = (os.path.splitext(filePath)[1])
    if (ext == '.zip'):
        Unzip(filePath , destinationPath)
    elif (ext == '.rar'):
        Unrar(filePath , destinationPath)



def Zip(contentsPath , filePath):
    print('Compressing...')
    newFilePath = filePath.replace('.rar','.zip')   #Program only supports zip
    newFilepath = AddFileExistsIndex(newFilePath)   #Add '(2)' or higher suffix if necessary

    length = len(contentsPath)

    zf = zipfile.ZipFile(newFilepath, "w")
    for folderName, _, filenames in os.walk(contentsPath):
       for filename in filenames:
            filePath = os.path.join(folderName, filename)   #Full filepath of file to inlude in zip
            arcPath  = filePath[length:]                    #Filepath inside zip archive (we don't need to recreate the full path)

            zf.write(filePath, arcname=arcPath)             #Add file to zip
    zf.close()
    print('Done')