
import sys
import winreg


def set_reg(reg_path, name, value):
    try:
        winreg.CreateKey(winreg.HKEY_CURRENT_USER, reg_path)
        registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_WRITE)
        winreg.SetValueEx(registry_key, name, 0, winreg.REG_SZ, value) # Type REG_SZ means null-terminated string
        winreg.CloseKey(registry_key)
        return(True)
    except WindowsError as e:
        print(str(e))
        return(False)



def get_reg(reg_path, name):
    try:
        registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_READ)
        value, regtype = winreg.QueryValueEx(registry_key, name)
        winreg.CloseKey(registry_key)
        return(value)
    except WindowsError as e:
        print(str(e))
        return(None)




def AddToContextMenu():
    """ Adds entries in context menus of many filetypes and folders to open them with this app """
    
    # name must be None so that the default key is modified. If we specified name="(Default)", it would create two (Default) keys.
    # command must be in the format "program.exe %1" or "py pathToScript %1".
    # In the Windows registry, %1 gets replaced by the path to the file whose context menu is opened
    
    appPath = sys.argv[0]   # path to this application. If it's a Python script, path to the entry point script
    command = f'py "{appPath}" "%1"'
    
    set_reg(reg_path=r"SOFTWARE\Classes\SystemFileAssociations\.zip\shell\ComicResizer\command", name=None, value=command)
    set_reg(reg_path=r"SOFTWARE\Classes\SystemFileAssociations\.rar\shell\ComicResizer\command", name=None, value=command)
    set_reg(reg_path=r"SOFTWARE\Classes\SystemFileAssociations\.cbz\shell\ComicResizer\command", name=None, value=command)
    set_reg(reg_path=r"SOFTWARE\Classes\SystemFileAssociations\.cbr\shell\ComicResizer\command", name=None, value=command)
    
    set_reg(reg_path=r"SOFTWARE\Classes\SystemFileAssociations\image\shell\ComicResizer\command", name=None, value=command)
    
    set_reg(reg_path=r"SOFTWARE\Classes\Directory\shell\ComicResizer\command", name=None, value=command)    # For when clicking a folder
    set_reg(reg_path=r"SOFTWARE\Classes\Directory\Background\shell\ComicResizer\command", name=None, value=command)    # For when clicking a folder's background
    
    print("Added to context menu")