from PySide6.QtWidgets import QMainWindow
from PySide6.QtGui import QCloseEvent
from GUI.MainContents import MainContents


class MainWindow(QMainWindow):
    """ Topmost GUI component """

    def __init__(self):
        super().__init__()
        
        # Window configuration
        self.setWindowTitle('Comic resizer')
        
        # Window contents
        self.contents = MainContents(self)
        self.setCentralWidget(self.contents)
        
        
    def closeEvent(self, event: QCloseEvent):
        """ Override QMainWindow's closeEvent to save settings on exit """
        self.contents.save_settings()
