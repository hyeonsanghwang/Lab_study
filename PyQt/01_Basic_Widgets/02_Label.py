"""
 * Requirements

pip install PyQt5

"""

import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLabel


def label_event(event):
    global label

    text = label.text()
    print(text)
    label.setText(text + "!!!!")


if __name__ == '__main__':
    app = QApplication(sys.argv)

    label = QLabel('Text')
    label.show()

    label.setStyleSheet("color: white; background-color:#0000ff")
    label.mouseReleaseEvent = label_event

    app.exec_()
