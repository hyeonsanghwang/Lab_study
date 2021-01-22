"""
 * Requirements

pip install PyQt5
pip install opencv-python

https://pytorch.org/

conda install pytorch torchvision torchaudio cudatoolkit=11.0 -c pytorch
or
conda install pytorch torchvision torchaudio cpuonly -c pytorch

"""

import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow

from test_tab import TabTest
from train_tab import TabTrain

form_class = uic.loadUiType('ui/main_window.ui')[0]
class MainWindow(QMainWindow, form_class):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.tab_train = TabTrain(self.statusBar())
        self.tab_test = TabTest(self.statusBar())

        self.tab_widget.addTab(self.tab_train, "Train")
        self.tab_widget.addTab(self.tab_test, "Test")

        self.tab_widget.setCurrentIndex(0)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec_()
