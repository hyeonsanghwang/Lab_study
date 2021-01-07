"""
 * Requirements

pip install PyQt5

"""

import sys

from PyQt5.Qt import Qt
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import QApplication, QTreeView, QAbstractItemView
from PyQt5.QtWidgets import QPushButton


def create_model():
    model = QStandardItemModel(0, 3)
    model.setHeaderData(0, Qt.Horizontal, "Name")
    model.setHeaderData(1, Qt.Horizontal, "Size")
    model.setHeaderData(2, Qt.Horizontal, "Type")
    return model


def click_event(index):
    global model

    data1 = model.item(index.row(), 0).data(Qt.DisplayRole)
    data2 = model.item(index.row(), 1).data(Qt.DisplayRole)
    data3 = model.item(index.row(), 2).data(Qt.DisplayRole)
    print(data1, data2, data3)


def remove_event():
    global model, tree_view
    model.removeRow(tree_view.currentIndex().row())


if __name__ == '__main__':
    app = QApplication(sys.argv)

    tree_view = QTreeView()
    model = create_model()
    tree_view.setModel(model)
    tree_view.show()

    tree_view.clicked.connect(click_event)

    model.insertRow(0)
    model.setData(model.index(0, 0), 'test.py')
    model.setData(model.index(0, 1), '100')
    model.setData(model.index(0, 2), 'python script')

    model.insertRow(0)
    model.setData(model.index(0, 0), 'image.jpg')
    model.setData(model.index(0, 1), '264')
    model.setData(model.index(0, 2), 'Image file')

    button = QPushButton('Remove')
    button.show()
    button.clicked.connect(remove_event)

    app.exec_()
