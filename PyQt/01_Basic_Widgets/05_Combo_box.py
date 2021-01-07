"""
 * Requirements

pip install PyQt5

"""

import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QComboBox


def combobox_event():
    global combobox

    index = combobox.currentIndex()
    text = combobox.currentText()
    print(index, " : ", text)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    combobox_items = ["Item1", "Item2", "Item3", "Item4"]
    combobox = QComboBox()
    for item in combobox_items:
        combobox.addItem(item)
    combobox.show()

    # combobox.currentIndexChanged.connect(combobox_event)

    app.exec_()
