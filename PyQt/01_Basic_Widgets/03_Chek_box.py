"""
 * Requirements

pip install PyQt5

"""

import sys

from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QRadioButton
from PyQt5.QtWidgets import QButtonGroup
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtWidgets import QProgressBar
from PyQt5.QtGui import QPixmap


def checkbox_event():
    global checkbox

    state = checkbox.isChecked()
    text = checkbox.text()
    print(state, text)
    checkbox.setText(text + "!!!!")


if __name__ == '__main__':
    app = QApplication(sys.argv)

    checkbox = QCheckBox('Check box')
    checkbox.show()

    checkbox.clicked.connect(checkbox_event)

    app.exec_()
