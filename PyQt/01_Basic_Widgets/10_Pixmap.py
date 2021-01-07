"""
 * Requirements

pip install PyQt5

"""

import sys

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QPushButton


def pixmap_event():
    global button
    pixmap = QPixmap('../images/image.jpg')
    label.setPixmap(pixmap)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    label = QLabel('Label')
    button = QPushButton('Button')
    button.clicked.connect(pixmap_event)
    label.show()
    button.show()

    app.exec_()
