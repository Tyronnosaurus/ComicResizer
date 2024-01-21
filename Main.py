from PySide6.QtWidgets import QApplication, QMessageBox
from GUI.MainWindow import MainWindow
import sys


def main():
    """ Entry point of the application """

    app = QApplication(sys.argv)
    w = MainWindow()
    
    try:
        app.exec()
        
    except Exception as e:
        dlg = QMessageBox()
        dlg.setWindowTitle("Error")
        dlg.setText(str(e))
        dlg.exec()


if __name__ == '__main__':
    main()