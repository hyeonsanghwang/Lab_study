import sys

import cv2
import numpy as np
from PyQt5 import QtGui
from PyQt5 import uic
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QApplication, QMainWindow


form_class = uic.loadUiType('window.ui')[0]
class MainWindow(QMainWindow, form_class):
    pixmap_change_signal = pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.video_thread = VideoThread()
        self.video_thread.image_change_signal.connect(self.set_image)
        self.video_thread.start()

    @pyqtSlot(np.ndarray)
    def set_image(self, frame):
        image = QtGui.QImage(frame, frame.shape[1], frame.shape[0], frame.shape[1] * 3, QtGui.QImage.Format_BGR888)
        pixmap = QtGui.QPixmap(image)
        self.label_image.setPixmap(pixmap)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.video_thread.capture = False
        self.video_thread.wait()


class VideoThread(QThread):
    image_change_signal = pyqtSignal(np.ndarray)

    def run(self):
        self.capture = True
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

        while self.capture:
            ret, frame = cap.read()
            if ret:
                self.image_change_signal.emit(frame)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec_()
