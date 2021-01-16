"""
 * Requirements

pip install PyQt5

"""

import sys
from PyQt5.QtWidgets import QApplication, QListWidget


def click_event():
    global list_widget
    print(list_widget.currentItem().text())
    print(list_widget.currentItem())


if __name__ == '__main__':
    app = QApplication(sys.argv)

    list_widget = QListWidget()
    list_widget.doubleClicked.connect(click_event)

    items = ["Item1", "Item2", "Item3", "Item4", "Item5", "Item6", "Item7", "Item8", "Item9"]
    for item in items:
        list_widget.addItem(item)

    list_widget.show()

    app.exec_()
