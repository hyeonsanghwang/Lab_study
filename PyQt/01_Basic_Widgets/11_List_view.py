"""
 * Requirements

pip install PyQt5

"""

import sys

from PyQt5.Qt import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QApplication, QListView
from PyQt5.QtWidgets import QPushButton


def create_model():
    model = QStandardItemModel(0, 3)
    model.setHeaderData(0, Qt.Horizontal, "Name")
    model.setHeaderData(1, Qt.Horizontal, "Size")
    model.setHeaderData(2, Qt.Horizontal, "Type")
    return model


def click_event(index):
    global model

    data = model.data(index)
    print(data)


def remove_event():
    global list_view, model

    index = list_view.currentIndex()
    model.removeRow(index.row())


if __name__ == '__main__':
    app = QApplication(sys.argv)

    list_view = QListView()
    list_view.show()

    model = QStandardItemModel()
    list_view_items = ["Item1", "Item2", "Item3", "Item4"]
    for item in list_view_items:
        model.appendRow(QStandardItem(item))
    list_view.setModel(model)
    list_view.clicked.connect(click_event)

    # button = QPushButton("Remove")
    # button.clicked.connect(remove_event)
    # button.show()

    app.exec_()
