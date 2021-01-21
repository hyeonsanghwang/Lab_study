"""
 * Requirements

pip install PyQt5

"""

import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog


form_class = uic.loadUiType('window.ui')[0]
class MainWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.actionLoad_file.triggered.connect(self.load_file_event)
        self.action_exit.triggered.connect(self.close)
        self.pushButton.clicked.connect(self.click_event)

    def load_file_event(self):
        self.statusbar.showMessage("Load file..")
        path = QFileDialog.getOpenFileName(self)
        print(path)
        self.statusbar.clearMessage()

    def click_event(self):
        print('click')


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec_()
