"""
 * Requirements

pip install PyQt5

"""

import sys
from PyQt5.QtWidgets import QApplication, QWidget


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = QWidget()
    window.show()

    app.exec_()
