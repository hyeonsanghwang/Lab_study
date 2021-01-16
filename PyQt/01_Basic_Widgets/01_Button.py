"""
 * Requirements

pip install PyQt5

"""

import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QPushButton


def button_event():
    print('button click')


if __name__ == '__main__':
    app = QApplication(sys.argv)

    button = QPushButton('Button')
    button.show()

    # button.clicked.connect(button_event)

    app.exec_()
