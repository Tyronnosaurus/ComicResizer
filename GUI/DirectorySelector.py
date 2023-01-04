from PySide6.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QPushButton, QFileDialog
from PySide6.QtCore import Signal, QObject


class DirectorySelector(QWidget):

    textChanged = Signal()      # Signal so that we don't have to connect to the internal QLineEdit.textChanged
    dialogReturned = Signal()   # Signal for when the dile/folder dialog returns a path


    def __init__(self, text=None, parent=None):
        super().__init__()

        layout = QHBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        
        # Non-writable lineEdit
        self.lineEdit = QLineEdit(text)
        self.lineEdit.setMinimumWidth(300)
        self.lineEdit.textChanged.connect(self.textChanged)    # The nested lineEdit.textChanged signal will trigger the DirectorySelector.textChanged signal
        layout.addWidget(self.lineEdit)

        # Button '...'
        button_selectDir = QPushButton("...")
        button_selectDir.setMaximumWidth(30)
        button_selectDir.clicked.connect(self.onClickedFileDialogButton)
        layout.addWidget(button_selectDir)

        self.setLayout(layout)



    def onClickedFileDialogButton(self) -> None:
        dir = QFileDialog.getExistingDirectory(self, "Open Directory", "", QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
        if (dir != ''):   # If user closes dialog, it returns ''. Ignore it and keep previous text
            self.lineEdit.setText(dir)
            self.dialogReturned.emit()
    

    def getText(self) -> None:
        return(self.lineEdit.text())

    def setText(self, text:str) -> None:
        self.lineEdit.setText(text)
