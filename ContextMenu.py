
# http://support.microsoft.com/kb/310516

import os

ARG='''Windows Registry Editor Version 5.00

[HKEY_LOCAL_MACHINE\SOFTWARE\Classes\SystemFileAssociations\.zip\shell]
[HKEY_LOCAL_MACHINE\SOFTWARE\Classes\SystemFileAssociations\.zip\shell\ComicResizer]
[HKEY_LOCAL_MACHINE\SOFTWARE\Classes\SystemFileAssociations\.zip\shell\ComicResizer\command]
@="py APP_PATH \\\"%1\\\""

[HKEY_LOCAL_MACHINE\SOFTWARE\Classes\SystemFileAssociations\.RAR\shell]
[HKEY_LOCAL_MACHINE\SOFTWARE\Classes\SystemFileAssociations\.RAR\shell\ComicResizer]
[HKEY_LOCAL_MACHINE\SOFTWARE\Classes\SystemFileAssociations\.RAR\shell\ComicResizer\command]
@="py APP_PATH \\\"%1\\\""

[HKEY_LOCAL_MACHINE\SOFTWARE\Classes\SystemFileAssociations\.cbz\shell]
[HKEY_LOCAL_MACHINE\SOFTWARE\Classes\SystemFileAssociations\.cbz\shell\ComicResizer]
[HKEY_LOCAL_MACHINE\SOFTWARE\Classes\SystemFileAssociations\.cbz\shell\ComicResizer\command]
@="py APP_PATH \\\"%1\\\""

[HKEY_LOCAL_MACHINE\SOFTWARE\Classes\SystemFileAssociations\.cbr\shell]
[HKEY_LOCAL_MACHINE\SOFTWARE\Classes\SystemFileAssociations\.cbr\shell\ComicResizer]
[HKEY_LOCAL_MACHINE\SOFTWARE\Classes\SystemFileAssociations\.cbr\shell\ComicResizer\command]
@="py APP_PATH \\\"%1\\\""

'''


def AddToContextMenu():

    appPath = "D:/Continguts/ComicResizer/ComicResizer.pyw"
    arg = ARG.replace("APP_PATH", appPath)

    #Prepare a regedit file
    f = open('edits.reg', 'w')
    f.write(arg)
    f.close()

    #Run file
    currentDir = os.getcwd()
    regPath = os.path.join(currentDir, 'edits.reg')

    cmdLine = 'regedit.exe ' + regPath

    os.system(cmdLine)

    #Delete regedit file
    #TODO