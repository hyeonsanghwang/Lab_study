"""
 * Requirements

pip install PyQt5

"""

import sys

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton

if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = QWidget()
    window.resize(500, 500)

    button = QPushButton('Button', window)
    button.move(100, 100)

    window.show()
    app.exec_()
