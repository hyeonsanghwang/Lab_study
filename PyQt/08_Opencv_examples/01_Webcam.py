import sys

import cv2
import numpy as np
from PyQt5 import QtGui
from PyQt5 import uic
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QApplication, QMainWindow


form_class = uic.loadUiType('webcam_window.ui')[0]
class MainWindow(QMainWindow, form_class):
    pixmap_change_signal = pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.disable_buttons(True)

        self.button_connect.clicked.connect(self.camera_connect_event)
        self.button_rgb.clicked.connect(lambda: self.button_event(self.button_rgb))
        self.button_gray.clicked.connect(lambda: self.button_event(self.button_gray))
        self.button_bin.clicked.connect(lambda: self.button_event(self.button_bin))

        self.video_thread = VideoThread()
        self.video_thread.image_change_signal.connect(self.set_image)

    @pyqtSlot(np.ndarray)
    def set_image(self, frame):
        if len(frame.shape) == 2:
            image = QtGui.QImage(frame, frame.shape[1], frame.shape[0], frame.shape[1], QtGui.QImage.Format_Grayscale8)
        else:
            image = QtGui.QImage(frame, frame.shape[1], frame.shape[0], frame.shape[1]*3, QtGui.QImage.Format_BGR888)
        pixmap = QtGui.QPixmap(image)
        self.label_image.setPixmap(pixmap)

    def camera_connect_event(self):
        if self.video_thread.capture:
            self.video_thread.stop()
            self.button_connect.setText('Connect')
            self.disable_buttons(True)
        else:
            self.video_thread.start()
            self.button_connect.setText('Disconnect')
            self.disable_buttons(False)

    def disable_buttons(self, disable):
        self.button_rgb.setDisabled(disable)
        self.button_gray.setDisabled(disable)
        self.button_bin.setDisabled(disable)

    def button_event(self, button):
        if button == self.button_rgb:
            self.video_thread.processing_mode = 0
        elif button == self.button_gray:
            self.video_thread.processing_mode = 1
        elif button == self.button_bin:
            self.video_thread.processing_mode = 2

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.video_thread.stop()


class VideoThread(QThread):
    image_change_signal = pyqtSignal(np.ndarray)
    capture = False
    processing_mode = 0  # 0: rgb / 1: gray / 2: bin

    def run(self):
        self.capture = True
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        while self.capture:
            ret, frame = cap.read()
            if not ret:
                break

            if self.processing_mode == 0:
                image = frame
            elif self.processing_mode == 1:
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            elif self.processing_mode == 2:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                image = (gray > 128).astype(np.uint8) * 255

            self.image_change_signal.emit(image)

    def stop(self):
        self.capture = False
        self.wait()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec_()
