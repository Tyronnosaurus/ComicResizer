
# http://support.microsoft.com/kb/310516    #How to edit registry with regedit files

import sys, os


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

[HKEY_LOCAL_MACHINE\SOFTWARE\Classes\Directory\shell]
[HKEY_LOCAL_MACHINE\SOFTWARE\Classes\Directory\shell\ComicResizer]
[HKEY_LOCAL_MACHINE\SOFTWARE\Classes\Directory\shell\ComicResizer\command]
@="py APP_PATH \\\"%1\\\""

[HKEY_LOCAL_MACHINE\SOFTWARE\Classes\SystemFileAssociations\image\shell]
[HKEY_LOCAL_MACHINE\SOFTWARE\Classes\SystemFileAssociations\image\shell\ComicResizer]
[HKEY_LOCAL_MACHINE\SOFTWARE\Classes\SystemFileAssociations\image\shell\ComicResizer\command]
@="py APP_PATH \\\"%1\\\""

'''



def AddToContextMenu():

    #In the registry command, replace APP_PATH with the actual path this program is being run from
    appPath = sys.argv[0]
    arg = ARG.replace("APP_PATH", appPath)

    #Generate path of reg file
    path = os.path.dirname(appPath) + '/edits.reg'

    #Create file
    f = open(path, 'w')
    f.write(arg)
    f.close()

    #Run file
    cmdLine = 'regedit.exe ' + path
    os.system(cmdLine)

    #Delete regedit file
    #TODO