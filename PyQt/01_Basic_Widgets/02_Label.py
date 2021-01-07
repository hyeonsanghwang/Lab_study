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


def set_widget_property(widget):
    widget.setStyleSheet("color: white; background-color:#0000ff")
    widget.mouseReleaseEvent = label_event


if __name__ == '__main__':
    app = QApplication(sys.argv)

    label = QLabel('Text')
    label.show()
    set_widget_property(label)

    app.exec_()
