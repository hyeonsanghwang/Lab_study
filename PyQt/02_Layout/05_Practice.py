"""
 * Requirements

pip install PyQt5

"""

import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QGridLayout


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = QWidget()
    window.show()

    app.exec_()
