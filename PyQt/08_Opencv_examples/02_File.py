import sys

from PyQt5.QtGui import QPixmap

try:
    from cv2 import cv2
except ImportError:
    pass
import numpy as np
from PyQt5 import QtGui
from PyQt5 import uic
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileSystemModel, QRadioButton

form_class = uic.loadUiType('file_window.ui')[0]
class MainWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.image = None
        self.set_tree_view()
        self.set_radio_button()


    def set_tree_view(self):
        self.root_path = '../'

        self.file_system_model = QFileSystemModel()
        self.tree_view.setModel(self.file_system_model)
        self.file_system_model.setRootPath(self.root_path)
        self.tree_view.setRootIndex(self.file_system_model.index(self.root_path))
        self.tree_view.setColumnWidth(0, 200)

        self.tree_view.setColumnHidden(1, True)
        self.tree_view.setColumnHidden(2, True)
        self.tree_view.setColumnHidden(3, True)

        self.tree_view.doubleClicked.connect(self.tree_view_double_clicked)

    def tree_view_double_clicked(self, index):
        if self.file_system_model.isDir(index):
            # print('Directory')
            pass
        else:
            path = self.file_system_model.filePath(index)
            self.image = cv2.imread(path)
            self.image_processing()

    def set_radio_button(self):
        self.radio_rgb.clicked.connect(self.image_processing)
        self.radio_gray.clicked.connect(self.image_processing)
        self.radio_bin.clicked.connect(self.image_processing)

    def image_processing(self):
        if self.image is None:
            return

        if self.radio_rgb.isChecked():
            processed = self.image
        elif self.radio_gray.isChecked():
            processed = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        else:
            gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            processed = (gray > 128).astype(np.uint8) * 255

        if len(processed.shape) == 2:
            show_image = QtGui.QImage(processed, processed.shape[1], processed.shape[0], processed.shape[1],
                                      QtGui.QImage.Format_Grayscale8)
        else:
            show_image = QtGui.QImage(processed, processed.shape[1], processed.shape[0], processed.shape[1] * 3,
                                      QtGui.QImage.Format_BGR888)
        self.label_image.setPixmap(QtGui.QPixmap(show_image))


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec_()
