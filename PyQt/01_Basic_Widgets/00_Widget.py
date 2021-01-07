"""
 * Requirements

pip install PyQt5

"""

import sys

from PyQt5.QtWidgets import QApplication, QWidget


def set_widget_property(widget):
    widget.setWindowTitle("GUI program")

    widget.move(2500, 200)
    widget.resize(500, 500)
    # or
    # widget.setGeometry(2500, 200, 500, 500)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    widget = QWidget()
    widget.show()
    # set_widget_property(widget)

    app.exec_()
