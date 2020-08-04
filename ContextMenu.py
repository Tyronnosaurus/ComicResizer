
# http://support.microsoft.com/kb/310516

import os

arg='''Windows Registry Editor Version 5.00

[HKEY_LOCAL_MACHINE\SOFTWARE\Classes\SystemFileAssociations\.zip\shell]
[HKEY_LOCAL_MACHINE\SOFTWARE\Classes\SystemFileAssociations\.zip\shell\ComicResizer]
[HKEY_LOCAL_MACHINE\SOFTWARE\Classes\SystemFileAssociations\.zip\shell\ComicResizer\command]
@="py D:/Continguts/ComicResizer/ComicResizer.pyw \\\"%1\\\""

[HKEY_LOCAL_MACHINE\SOFTWARE\Classes\SystemFileAssociations\.RAR\shell]
[HKEY_LOCAL_MACHINE\SOFTWARE\Classes\SystemFileAssociations\.RAR\shell\ComicResizer]
[HKEY_LOCAL_MACHINE\SOFTWARE\Classes\SystemFileAssociations\.RAR\shell\ComicResizer\command]
@="py D:/Continguts/ComicResizer/ComicResizer.pyw \\\"%1\\\""


'''

def AddToContextMenu():

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