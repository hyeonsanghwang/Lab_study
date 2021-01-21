import sys


import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.datasets as dsets
import torchvision.transforms as transforms

import cv2
import numpy as np
from PyQt5 import QtGui
from PyQt5 import uic
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot, QDir
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileSystemModel, QTreeView, QMessageBox, QLabel, QProgressBar
import threading

form_class = uic.loadUiType('mnist_window.ui')[0]
class MainWindow(QMainWindow, form_class):
    pixmap_change_signal = pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.train_thread = None

        self.set_tree_view()
        self.init_progress_bar()
        self.button_start.clicked.connect(self.start_training)

    def set_tree_view(self):
        self.file_model = QFileSystemModel()
        self.tree_view.setModel(self.file_model)

        self.root_path = "../"
        self.file_model.setRootPath(self.root_path)
        self.tree_view.setRootIndex(self.file_model.index(self.root_path))

        self.tree_view.setColumnHidden(1, True)
        self.tree_view.setColumnHidden(2, True)
        self.tree_view.setColumnHidden(3, True)

    def init_progress_bar(self, step=1):
        self.progress_bar.setRange(0, step)
        self.progress_bar.reset()

    def update_progress_bar(self):
        val = self.progress_bar.value()
        self.progress_bar.setValue(val + 1)

    def start_training(self):
        data_path = self.file_model.filePath(self.tree_view.currentIndex())
        batch_size = self.line_edit_batch_size.text()
        epochs = self.line_edit_epochs.text()
        lr = self.line_edit_learning_rate.text()

        if data_path and batch_size and epochs and lr:
            batch_size = int(batch_size)
            epochs = int(epochs)
            lr = float(lr)

            self.button_start.setDisabled(True)
            self.init_progress_bar(epochs)
            self.train_thread = threading.Thread(target=self.__train, args=(data_path, batch_size, epochs, lr))
            self.train_thread.start()
        else:
            QMessageBox.critical(self,
                                 'Error',
                                 '폴더 및 파라미터를 설정해주세요.',
                                 QMessageBox.Ok)

    def __train(self, path, batch_size, epochs, lr):
        self.stop_train = False

        self.update_progress_bar()
        devices_id = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        torch.cuda.set_device(devices_id)

        train_dataset = dsets.MNIST(root=path, train=True, transform=transforms.ToTensor(), download=False)
        train_loader = torch.utils.data.DataLoader(dataset=train_dataset, batch_size=batch_size, shuffle=True)

        model = CNN()
        if devices_id == type([]):  # -> GPU
            model = nn.DataParallel(model, device_ids=devices_id).cuda()
        else:
            model = nn.DataParallel(model, device_ids=[devices_id]).cuda()

        criterion = torch.nn.CrossEntropyLoss()
        optimizer = torch.optim.SGD(model.parameters(), lr=lr)

        losses = []

        for epoch in range(epochs):
            for i, (images, labels) in enumerate(train_loader):
                images = images.to(devices_id)
                labels = labels.to(devices_id)

                optimizer.zero_grad()
                outputs = model(images)
                loss = criterion(outputs, labels)
                loss.backward()
                optimizer.step()

                losses.append(loss.item())
                # self.show_loss_graph(losses)
                if self.stop_train:
                    break
            self.update_progress_bar()
            if self.stop_train:
                break

        self.button_start.setDisabled(False)
        QMessageBox.information(self, 'Info', '학습 완료', QMessageBox.Ok)
        print('??????????')


    def show_loss_graph(self, losses):
        signal = np.array(losses)
        cv2.normalize(signal, signal, 1, 0, cv2.NORM_MINMAX)
        signal = 1 - signal

        h, w = self.label_graph.height(), self.label_graph.width()
        l = signal.shape[0]
        frame = np.ones((h, w, 3), np.uint8) * 255
        for i in range(l-1):
            sy = int(signal[i] * h)
            ey = int(signal[i+1] * h)
            sx = int(i*(w/l))
            ex = int((i+1)*(w/l))

            cv2.line(frame, (sx, sy), (ex, ey), (0,0, 255), 2)
        self.set_image(frame)

    def set_image(self, frame):
        image = QtGui.QImage(frame, frame.shape[1], frame.shape[0], frame.shape[1] * 3, QtGui.QImage.Format_BGR888)
        pixmap = QtGui.QPixmap(image)
        self.label_graph.setPixmap(pixmap)

    def __stop_train(self):
        self.stop_train = True
        if self.train_thread != None:
            self.train_thread.join()
            self.train_thread = None

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.__stop_train()


class CNN(nn.Module):
    def __init__(self):
        super(CNN, self).__init__()
        self.conv1 = nn.Conv2d(1, 10, kernel_size=5)
        self.conv2 = nn.Conv2d(10, 20, kernel_size=5)
        self.mp = nn.MaxPool2d(2)
        self.fc = nn.Linear(320, 10)

    def forward(self, x):
        in_size = x.size(0)
        x = F.relu(self.mp(self.conv1(x)))
        x = F.relu(self.mp(self.conv2(x)))
        x = x.view(in_size, -1)  # flatten the tensor
        outputs = self.fc(x)
        return outputs



if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    try:
        app.exec_()
    except Exception as e:
        print(e)
