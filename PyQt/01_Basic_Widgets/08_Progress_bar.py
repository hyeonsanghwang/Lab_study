"""
 * Requirements

pip install PyQt5

"""

import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QProgressBar
from PyQt5.QtWidgets import QPushButton


def progress_event():
    global progress

    val = progress.value()
    progress.setValue(val+10)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    progress = QProgressBar()

    progress.setRange(1, 100)
    progress.reset()
    # or
    # progress.setRange(0, 0)

    progress.show()

    button = QPushButton('Button')
    button.show()
    button.clicked.connect(progress_event)

    app.exec_()
