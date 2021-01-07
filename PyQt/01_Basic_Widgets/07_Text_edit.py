"""
 * Requirements

pip install PyQt5

"""

import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QTextEdit


def text_edit_event():
    global text_edit

    print(text_edit.toPlainText())
    text_edit.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    text_edit = QTextEdit()
    text_edit.show()

    button = QPushButton('Button')
    button.show()
    button.clicked.connect(text_edit_event)

    app.exec_()
