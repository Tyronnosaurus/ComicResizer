from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QCheckBox, QPushButton, QSpacerItem, QSizePolicy
from PySide6.QtCore import QSettings
from PySide6.QtGui import QCloseEvent

from GUI.Separators import HorizontalLineSeparator
from GUI.DirectorySelector import DirectorySelector

import GlobalControl

import os
import sys
from ContextMenu import AddToContextMenu, RemoveFromContextMenu



class MainWindow(QMainWindow):
    """ Topmost GUI component """

    def __init__(self):
        super().__init__()
        
        # Window configuration
        self.setWindowTitle('Comic resizer')
        
        # Window contents
        self.contents = Contents(self)
        self.setCentralWidget(self.contents)
        
        self.show()
        
        
        
    def closeEvent(self, event: QCloseEvent):
        """ Override QMainWindow's closeEvent to save settings on exit """
        self.contents.save_settings()
        




class Contents(QWidget):
    """ Contents of the main window """
    
    def __init__(self, parent):
        super().__init__(parent)


        # ---- Source path & desired width ---
        vLayout = QVBoxLayout()

        vLayout.addWidget(QLabel("Source"))

        self.srcLineEdit = DirectorySelector()
        if (len(sys.argv)>1): self.srcLineEdit.setText(sys.argv[1]) # If opened from a context menu, automatically write the 2nd argument (path to file) in the src input
        vLayout.addWidget(self.srcLineEdit)

        hLayoutWidth = QHBoxLayout()
        hLayoutWidth.addWidget(QLabel("Width:"))

        self.widthLineEdit = QLineEdit()
        self.widthLineEdit.setFixedWidth(50)
        hLayoutWidth.addWidget(self.widthLineEdit)

        hLayoutWidth.addWidget(QLabel("px"))

        hLayoutWidth.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding))

        vLayout.addLayout(hLayoutWidth)

        vLayout.addWidget(HorizontalLineSeparator())


        # ---- Options ----
        self.checkBoxDeleteOriginal = QCheckBox("Delete original")
        vLayout.addWidget(self.checkBoxDeleteOriginal)

        self.checkBoxDeleteTempFolder = QCheckBox("Delete temp folder")
        vLayout.addWidget(self.checkBoxDeleteTempFolder)
        
        self.checkBoxSmartResizing = QCheckBox("Smart resizing (detect doublepages, etc.)")
        vLayout.addWidget(self.checkBoxSmartResizing)
        
        self.checkBoxOnlyReduce = QCheckBox("Only reduce size, don't increase")
        vLayout.addWidget(self.checkBoxOnlyReduce)

        vLayout.addWidget(HorizontalLineSeparator())


        # ---- 'Resize' buttons ----
        pushButtonResize = QPushButton("Resize")
        pushButtonResize.setFixedHeight(50)
        vLayout.addWidget(pushButtonResize)

        hLayoutSubsteps = QHBoxLayout()
        hLayoutSubsteps.addWidget(QLabel("Substeps:"))

        pushButtonResize1 = QPushButton("1/2\nExtract && preview")  # Qt uses '&' to set keyboard shortcuts. We need two (&&) so that it appears correctly
        hLayoutSubsteps.addWidget(pushButtonResize1)

        pushButtonResize2 = QPushButton("2/2\nResize && compress")
        hLayoutSubsteps.addWidget(pushButtonResize2)

        vLayout.addLayout(hLayoutSubsteps)

        vLayout.addWidget(HorizontalLineSeparator())


        # ---- Close when finished, context menu button ----
        hLayoutBottom = QHBoxLayout()
        self.checkBoxCloseWhenFinished = QCheckBox("Close when finished")
        hLayoutBottom.addWidget(self.checkBoxCloseWhenFinished)

        hLayoutBottom.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding))

        pushButtonAddToContexMenu = QPushButton("Add context\nmenu item")
        hLayoutBottom.addWidget(pushButtonAddToContexMenu)
        
        pushButtonRemoveFromContexMenu = QPushButton("Delete context\nmenu item")
        hLayoutBottom.addWidget(pushButtonRemoveFromContexMenu)

        vLayout.addLayout(hLayoutBottom)

        self.setLayout(vLayout)


        # Connect buttons to functions
        pushButtonResize.clicked.connect(self.Resize)
        pushButtonResize1.clicked.connect(self.ExtractAndPreview)
        pushButtonResize2.clicked.connect(self.ResizeAndCompress)
        pushButtonAddToContexMenu.clicked.connect(AddToContextMenu)
        pushButtonRemoveFromContexMenu.clicked.connect(RemoveFromContextMenu)
        
        # Settings. Must be at the end (because at start, the checkboxes and other inputs still don't exist)
        self.load_settings()
    
    
    
    def Resize(self) -> None:
        """ Runs the whole resizing process """
        filePath = self.srcLineEdit.getText()
        newWidth = int(self.widthLineEdit.text())
        
        self.prepareSettingsObject()
        
        GlobalControl.ResizeComic(filePath, newWidth, self.settings)
        
        
    # Instead of resizing in one go, we also have the option to do it in 2 steps to preview the images before resizing them (only useful for compressed files)
    
    def ExtractAndPreview(self) -> None:
        """ Substep 1 of 2: extracts contents of the archive into a temporal folder and opens it so that the user can preview and edit images before resizing """
        filePath:str = self.srcLineEdit.getText()
        newWidth:int = int(self.widthLineEdit.text())
        self.prepareSettingsObject()
        
        GlobalControl.ExtractAndPreview(filePath , self.settings)
        
    
    def ResizeAndCompress(self) -> None:
        """ Substep 2 of 2: resizes the files in the temporal folder and compresses them into an archive """
        filePath:str = self.srcLineEdit.getText()
        newWidth:int = int(self.widthLineEdit.text())
        self.prepareSettingsObject()
        
        GlobalControl.ResizeAndCompress(filePath, newWidth, self.settings)
    
    
        
    def prepareSettingsObject(self):
        """ Get all user settings from the GUI into a single 'settings' object """
        self.settings.deleteOriginal    = self.checkBoxDeleteOriginal.isChecked()
        self.settings.deleteTemp        = self.checkBoxDeleteTempFolder.isChecked()
        self.settings.smartResize       = self.checkBoxSmartResizing.isChecked()
        self.settings.onlyReduce        = self.checkBoxOnlyReduce.isChecked()
        self.settings.closeWhenFinished = self.checkBoxCloseWhenFinished.isChecked()
        
        


    def load_settings(self):
        settings = QSettings(self.get_settings_filepath(), QSettings.IniFormat)

        self.widthLineEdit.setText(settings.value("Width", 1280, str))
        self.checkBoxDeleteOriginal.setChecked(settings.value("DeleteOriginal", True, bool))
        self.checkBoxDeleteTempFolder.setChecked(settings.value("DeleteTempFolder", True, bool))
        self.checkBoxSmartResizing.setChecked(settings.value("SmartResizing", True, bool))
        self.checkBoxOnlyReduce.setChecked(settings.value("OnlyReduce", True, bool))
        self.checkBoxCloseWhenFinished.setChecked(settings.value("CloseWhenFinished", False, bool))

        

    def save_settings(self):
        settings = QSettings(self.get_settings_filepath(), QSettings.IniFormat)
        
        settings.setValue("Width", self.widthLineEdit.text())
        settings.setValue("DeleteOriginal", self.checkBoxDeleteOriginal.isChecked())
        settings.setValue("DeleteTempFolder", self.checkBoxDeleteTempFolder.isChecked())
        settings.setValue("SmartResizing", self.checkBoxSmartResizing.isChecked())
        settings.setValue("OnlyReduce", self.checkBoxOnlyReduce.isChecked())
        settings.setValue("CloseWhenFinished", self.checkBoxCloseWhenFinished.isChecked())
        
        
    def get_settings_filepath(self) -> str:
        app_path = sys.argv[0]   # path to this application. If it's a Python script, path to the entry point script
        app_path = os.path.dirname(app_path)   # The path contains the script file, but we only want the directory
        return(os.path.join(app_path, "settings.ini"))
