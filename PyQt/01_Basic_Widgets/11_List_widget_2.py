"""
 * Requirements

pip install PyQt5

"""

import sys

from PyQt5.QtWidgets import QApplication, QListWidget, QListWidgetItem, QPushButton


if __name__ == '__main__':
    app = QApplication(sys.argv)

    list_widget = QListWidget()

    for i in range(10):
        item = QListWidgetItem()
        button = QPushButton('Button'+str(i+1))
        item.setSizeHint(button.sizeHint())
        list_widget.addItem(item)
        list_widget.setItemWidget(item, button)

    list_widget.show()

    app.exec_()
