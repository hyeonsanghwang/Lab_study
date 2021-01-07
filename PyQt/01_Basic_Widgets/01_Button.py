"""
 * Requirements

pip install PyQt5

"""

import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QPushButton


def button_event():
    print('button click')


def set_widget_property(widget):
    widget.clicked.connect(button_event)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    button = QPushButton('Button')
    button.show()
    # set_widget_property(button)

    app.exec_()
