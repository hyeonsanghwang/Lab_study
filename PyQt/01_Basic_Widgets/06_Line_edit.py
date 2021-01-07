"""
 * Requirements

pip install PyQt5

"""

import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLineEdit


def line_edit_event():
    global line_edit

    print(line_edit.text())
    line_edit.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    line_edit = QLineEdit()
    line_edit.show()

    # button = QPushButton('Button')
    # button.show()
    # button.clicked.connect(line_edit_event)

    app.exec_()
