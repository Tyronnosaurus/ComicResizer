from configparser import ConfigParser
import os


class Settings_class:
    def __init__(self):
        self.deleteOriginal:    bool = False
        self.deleteTemp:        bool = False
        self.smartResize:       bool = False
        self.onlyReduce:        bool = False
        self.closeWhenFinished: bool = False
        
        #Path of the external file to save and load settings. We need dirname() and realpath() because otherwise, when
        #executing from a context menu, the config.ini file is saved in the comic's folder, not the application's folder.
        self.settingsPath = os.path.dirname(os.path.realpath(__file__)) + '/config.ini'



    def Load(self):

        if(os.path.exists(self.settingsPath)):
            try:
                config = ConfigParser()

                config.read(self.settingsPath)

                self.deleteOriginal    = config.getboolean('main', 'deleteOriginal')
                self.deleteTemp        = config.getboolean('main', 'deleteTemp')
                self.smartResize       = config.getboolean('main', 'smartResize')
                self.onlyReduce        = config.getboolean('main', 'onlyReduce')
                self.closeWhenFinished = config.getboolean('main', 'closeWhenFinished')

            except:
                #In case a new setting has been implemented but it didn't exist when config.ini was saved last time
                pass

        

    def Save(self):
        print("Saving settings")
        config = ConfigParser()
        
        config.read(self.settingsPath)
        if(not config.has_section('main')): config.add_section('main')

        config.set(section='main', option='deleteOriginal'   , value=str(self.deleteOriginal))
        config.set(section='main', option='deleteTemp'       , value=str(self.deleteTemp))
        config.set(section='main', option='smartResize'      , value=str(self.smartResize))
        config.set(section='main', option='onlyReduce'       , value=str(self.onlyReduce))
        config.set(section='main', option='closeWhenFinished', value=str(self.closeWhenFinished))

        with open(self.settingsPath, 'w') as f:
            config.write(f)



