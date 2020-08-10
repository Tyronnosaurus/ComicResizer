import tkinter as tk
from configparser import ConfigParser
import os


class Settings_class:
    #These settings are Tkinter objects (not normal bools). You need to use get() to obtain the actual values.
    def __init__(self):
        self.deleteOriginal    = tk.BooleanVar()
        self.deleteTemp        = tk.BooleanVar()
        self.smartResize       = tk.BooleanVar()
        self.onlyReduce        = tk.BooleanVar()
        self.closeWhenFinished = tk.BooleanVar()
        
        #Path of the external file to save and load settings. We need dirname() and realpath() because otherwise, when
        #executing from a context menu, the config.ini file is saved in the comic's folder, not the application's folder.
        self.settingsPath = os.path.dirname(os.path.realpath(__file__)) + '/config.ini'


    def Load(self):

        if(os.path.exists(self.settingsPath)):
            try:
                config = ConfigParser()

                config.read(self.settingsPath)

                self.deleteOriginal.set(    config.getboolean('main', 'deleteOriginal') )
                self.deleteTemp.set(        config.getboolean('main', 'deleteTemp') )
                self.smartResize.set(       config.getboolean('main', 'smartResize') )
                self.onlyReduce.set(        config.getboolean('main', 'onlyReduce') )
                self.closeWhenFinished.set( config.getboolean('main', 'closeWhenFinished') )

            except:
                #In case a new setting has been implemented but it didn't exist when config.ini was saved last time
                pass

        

    def Save(self):
        config = ConfigParser()
        
        config.read(self.settingsPath)
        if(not config.has_section('main')): config.add_section('main')

        config.set(section='main', option='deleteOriginal'   , value=str(self.deleteOriginal.get()))
        config.set(section='main', option='deleteTemp'       , value=str(self.deleteTemp.get()))
        config.set(section='main', option='smartResize'      , value=str(self.smartResize.get()))
        config.set(section='main', option='onlyReduce'       , value=str(self.onlyReduce.get()))
        config.set(section='main', option='closeWhenFinished', value=str(self.closeWhenFinished.get()))

        with open(self.settingsPath, 'w') as f:
            config.write(f)



