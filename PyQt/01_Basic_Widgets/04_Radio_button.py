"""
 * Requirements

pip install PyQt5

"""

import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QButtonGroup
from PyQt5.QtWidgets import QRadioButton


def radio1_event():
    global group1
    print("Button ID : ", group1.checkedId(), " / Button text : ", group1.checkedButton().text())


def radio2_event():
    global group2
    print("Button ID : ", group2.checkedId(), " / Button text : ", group2.checkedButton().text())


if __name__ == '__main__':
    app = QApplication(sys.argv)

    radio1_1 = QRadioButton('Radio 1_1')
    radio1_2 = QRadioButton('Radio 1_2')
    radio2_1 = QRadioButton('Radio 2_1')
    radio2_2 = QRadioButton('Radio 2_2')

    radio1_1.setGeometry(250, 100, 200, 50)
    radio1_2.setGeometry(500, 100, 200, 50)
    radio2_1.setGeometry(750, 100, 200, 50)
    radio2_2.setGeometry(1000, 100, 200, 50)

    group1 = QButtonGroup()
    group1.addButton(radio1_1, 1)
    group1.addButton(radio1_2, 2)

    group2 = QButtonGroup()
    group2.addButton(radio2_1, 1)
    group2.addButton(radio2_2, 2)

    radio1_1.show()
    radio1_2.show()
    radio2_1.show()
    radio2_2.show()

    # group1.buttonClicked.connect(radio1_event)
    # group2.buttonClicked.connect(radio2_event)

    app.exec_()
