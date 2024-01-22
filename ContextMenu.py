
import sys
import winreg
from winreg import HKEYType, EnumKey
from typing import Union



ROOT_HKEY = winreg.HKEY_CURRENT_USER


def set_reg(reg_path: str, name: str, value: Union[str,int]) -> bool:
    try:
        winreg.CreateKey(ROOT_HKEY, reg_path)
        registry_key = winreg.OpenKey(ROOT_HKEY, reg_path, 0, winreg.KEY_WRITE)
        winreg.SetValueEx(registry_key, name, 0, winreg.REG_SZ, value) # Type REG_SZ means null-terminated string
        winreg.CloseKey(registry_key)
        return(True)
    except WindowsError as e:
        print(str(e))
        return(False)



def get_reg(reg_path, name):
    try:
        registry_key = winreg.OpenKey(ROOT_HKEY, reg_path, 0, winreg.KEY_READ)
        value, regtype = winreg.QueryValueEx(registry_key, name)
        winreg.CloseKey(registry_key)
        return(value)
    except WindowsError as e:
        print(str(e))
        return(None)
    
    
    
def delete_subkey(parent_key_name: str, subkey_name: str):
    """ Deletes key from Windows registry.

    Args:
        parent_key_name (str): parent of the key we want to delete. This will not be deleted. 
        subkey_name (str): key we want to delete. If it has subkeys, they will also be deleted.
    """


    # We've got the parent's key as a string, but we need to open it   
    parent_key:HKEYType = winreg.OpenKey(key=ROOT_HKEY, sub_key=parent_key_name, reserved=0, access=winreg.KEY_READ)

    delete_subkey_recursive(parent_key, subkey_name)



def delete_subkey_recursive(key: Union[HKEYType, int], subkey_name: str):
    """
    winreg.delete_key() can't delete a key if it has subkeys, so we must delete recursively from the bottom.
    See: https://stackoverflow.com/a/75241885

    Args:
        key (Union[HKEYType, int]): An already opened key, or one of the HKEY_ constants.
        subkey_name (str): name of the subkey to delete, which may or may not be empty.
    """
    with winreg.OpenKey(key, subkey_name) as subkey:
        while True:
            try:
                sub_sub_key_name = EnumKey(subkey, 0)
                delete_subkey_recursive(key=subkey, subkey_name=sub_sub_key_name)
            except OSError: # According to documentation, catching the exception is the recommended way to break the loop
                break

    winreg.DeleteKey(key, subkey_name)







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
    
    command = f'py "{appPath}" "%V"'  # When context menu is opened from a folder's background, instead of %1 we use %V to get the folder's path
    set_reg(reg_path=r"SOFTWARE\Classes\Directory\Background\shell\ComicResizer\command", name=None, value=command)    # For when clicking a folder's background
    
    print("Added entries to context menu")
    
    
    
def RemoveFromContextMenu():
    """ Removes the context menu entries for this program by deleting the Windows registry keys we had added with AddToContextMenu() """
    delete_subkey(parent_key_name=r"SOFTWARE\Classes\SystemFileAssociations\.zip\shell", subkey_name=r"ComicResizer")
    delete_subkey(parent_key_name=r"SOFTWARE\Classes\SystemFileAssociations\.rar\shell", subkey_name=r"ComicResizer")
    delete_subkey(parent_key_name=r"SOFTWARE\Classes\SystemFileAssociations\.cbz\shell", subkey_name=r"ComicResizer")
    delete_subkey(parent_key_name=r"SOFTWARE\Classes\SystemFileAssociations\.cbr\shell", subkey_name=r"ComicResizer")
    
    delete_subkey(parent_key_name=r"SOFTWARE\Classes\SystemFileAssociations\image\shell", subkey_name=r"ComicResizer")
    
    delete_subkey(parent_key_name=r"SOFTWARE\Classes\Directory\shell", subkey_name=r"ComicResizer")
    delete_subkey(parent_key_name=r"SOFTWARE\Classes\Directory\Background\shell", subkey_name=r"ComicResizer")