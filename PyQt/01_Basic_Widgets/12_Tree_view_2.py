"""
 * Requirements

pip install PyQt5

"""

import sys

from PyQt5.Qt import Qt
from PyQt5.QtCore import QDir
from PyQt5.QtGui import QPixmap, QStandardItemModel
from PyQt5.QtWidgets import QApplication, QTreeView, QFileSystemModel
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QPushButton


def double_click_event(index):
    global model, label

    if model.isDir(index):
        print('Directory')
    else:
        path = model.filePath(index)
        label.setPixmap(QPixmap(path))


if __name__ == '__main__':
    app = QApplication(sys.argv)

    tree_view = QTreeView()
    tree_view.show()

    model = QFileSystemModel()
    tree_view.setModel(model)

    root_path = "../"
    model.setRootPath(root_path)
    tree_view.setRootIndex(model.index(root_path))
    tree_view.setColumnWidth(0, 400)
    tree_view.resize(700, 500)

    tree_view.setColumnHidden(1, True)
    tree_view.setColumnHidden(2, True)
    tree_view.setColumnHidden(3, True)

    tree_view.doubleClicked.connect(double_click_event)

    label = QLabel("label")
    label.show()

    app.exec_()
