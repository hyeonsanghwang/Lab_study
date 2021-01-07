"""
 * Requirements

pip install PyQt5

"""

import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QSlider


def slider_horizon_event():
    global slider_horizon
    print(slider_horizon.value())


def slider_vertical_event():
    global slider_vertical
    print(slider_vertical.value())


if __name__ == '__main__':
    app = QApplication(sys.argv)

    slider_horizon = QSlider(Qt.Horizontal)
    slider_horizon.setRange(0, 200)
    slider_horizon.show()
    slider_horizon.valueChanged.connect(slider_horizon_event)

    slider_vertical = QSlider(Qt.Vertical)
    slider_vertical.setRange(0, 200)
    slider_vertical.show()
    slider_vertical.valueChanged.connect(slider_vertical_event)

    app.exec_()
