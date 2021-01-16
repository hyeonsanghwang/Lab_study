import sys

try:
    from cv2 import cv2
except ImportError:
    pass
import numpy as np
from PyQt5 import QtGui
from PyQt5 import uic
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot, QDir
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileSystemModel

form_class = uic.loadUiType('window.ui')[0]
class MainWindow(QMainWindow, form_class):
    pixmap_change_signal = pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.path = QDir.rootPath()

        self.dir_model = QFileSystemModel()
        self.dir_model.setRootPath('')
        self.dir_model.setFilter(QDir.NoDotAndDotDot | QDir.AllDirs)
        self.tree_view.setModel(self.dir_model)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec_()
