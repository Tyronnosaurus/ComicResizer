from PySide6.QtWidgets import QApplication
from GUI.MainWindow import MainWindow
import sys


def main():
    """ Entry point of the application """

    app = QApplication(sys.argv)
    w = MainWindow()
    app.exec()


if __name__ == '__main__':
    main()