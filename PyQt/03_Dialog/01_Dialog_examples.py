"""
 * Requirements

pip install PyQt5

"""

import sys

from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QLabel
from PyQt5.QtWidgets import QInputDialog, QMessageBox, QFileDialog
from PyQt5.QtGui import QPixmap


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.resize(500, 500)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Message box
        self.button_message_box = QPushButton('Message box')
        self.layout.addWidget(self.button_message_box)
        self.button_message_box.clicked.connect(self.message_box_event)

        # Input dialog
        self.button_input_dialog = QPushButton('Input dialog')
        self.label_text = QLabel()
        self.layout.addWidget(self.button_input_dialog)
        self.layout.addWidget(self.label_text)
        self.button_input_dialog.clicked.connect(self.input_dialog_event)

        # File dialog
        self.button_file_dialog = QPushButton('File dialog')
        self.label_image = QLabel()
        self.pixmap = QPixmap()
        self.layout.addWidget(self.button_file_dialog)
        self.layout.addWidget(self.label_image)
        self.button_file_dialog.clicked.connect(self.file_dialog_event)

    def message_box_event(self):
        QMessageBox.about(self, 'About box', 'Message')

        ret = QMessageBox.information(self, 'Information box', 'Message', QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Ok)
        if ret == QMessageBox.Ok:
            print('Information box : ok')
        elif ret == QMessageBox.Cancel:
            print('Information box : cancel')

        ret = QMessageBox.warning(self, 'Warning box', 'Message', QMessageBox.Discard | QMessageBox.Cancel, QMessageBox.Discard)
        if ret == QMessageBox.Discard:
            print('Warning box : Discard')
        elif ret == QMessageBox.Cancel:
            print('Warning box : cancel')

        ret = QMessageBox.question(self, 'Question box', 'Message', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if ret == QMessageBox.Yes:
            print('Question box : yes')
        elif ret == QMessageBox.No:
            print('Question box : no')

        ret = QMessageBox.critical(self, 'Critical box', 'Message', QMessageBox.Discard | QMessageBox.Cancel, QMessageBox.Cancel)
        if ret == QMessageBox.Discard:
            print('Warning box : Discard')
        elif ret == QMessageBox.Cancel:
            print('Warning box : cancel')

    def input_dialog_event(self):
        text, ret = QInputDialog.getText(self, 'Input dialog', 'input : ')
        if ret:
            self.label_text.setText(text)

    def file_dialog_event(self):
        ret = QFileDialog.getOpenFileName(self, 'Select file')
        print(ret)

        path = ret[0]
        self.pixmap.load(path)
        self.label_image.setPixmap(self.pixmap)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec_()
