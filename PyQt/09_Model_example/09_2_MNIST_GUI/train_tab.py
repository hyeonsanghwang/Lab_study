import cv2
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from PyQt5 import QtGui
from PyQt5 import uic
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QFileSystemModel, QMessageBox, QFileDialog, QWidget
from torch.utils.data import DataLoader
from torchvision import datasets
from torchvision import transforms

form_class = uic.loadUiType('ui/train_tab.ui')[0]
class TabTrain(QWidget, form_class):
    def __init__(self, status_bar):
        super().__init__()
        self.setupUi(self)
        self.status_bar = status_bar

        # Initialize
        self.set_tree_view()
        self.set_widgets()
        self.set_events()

    # Initialize
    def set_tree_view(self):
        self.root_path = "../../"
        self.file_model = QFileSystemModel()
        self.file_model.setRootPath(self.root_path)

        self.tree_view.setModel(self.file_model)
        self.tree_view.setRootIndex(self.file_model.index(self.root_path))
        self.tree_view.setColumnHidden(1, True)
        self.tree_view.setColumnHidden(2, True)
        self.tree_view.setColumnHidden(3, True)

    def set_widgets(self):
        self.button_save.setDisabled(True)
        self.reset_progress_bar()

    def reset_progress_bar(self, step=1):
        self.progress_bar.setRange(0, step)
        self.progress_bar.reset()

    def set_events(self):
        self.button_start.clicked.connect(self.on_click_start)
        self.button_save.clicked.connect(self.on_click_save)

    # Control widgets
    def disable_widgets(self):
        self.button_start.setDisabled(True)
        self.line_edit_batch_size.setDisabled(True)
        self.line_edit_epochs.setDisabled(True)
        self.line_edit_learning_rate.setDisabled(True)

    def enable_widgets(self):
        self.button_start.setDisabled(False)
        self.line_edit_batch_size.setDisabled(False)
        self.line_edit_epochs.setDisabled(False)
        self.line_edit_learning_rate.setDisabled(False)

    def set_image(self, frame, label):
        image = QtGui.QImage(frame, frame.shape[1], frame.shape[0], frame.shape[1] * 3, QtGui.QImage.Format_BGR888)
        pixmap = QtGui.QPixmap(image)
        label.setPixmap(pixmap)

    # Events
    def on_click_start(self):
        data_path = self.file_model.filePath(self.tree_view.currentIndex())
        batch_size = self.line_edit_batch_size.text()
        epochs = self.line_edit_epochs.text()
        lr = self.line_edit_learning_rate.text()

        if data_path and batch_size and epochs and lr:
            self.data_path = data_path
            self.batch_size = int(batch_size)
            self.epochs = int(epochs)
            self.lr = float(lr)

            # Create train thread
            self.thread_train = TrainThread()
            self.thread_train.set_parameters(self.data_path, self.batch_size, self.epochs, self.lr)

            # Set signal / slot
            self.thread_train.start_signal.connect(self.on_start_train)
            self.thread_train.change_state_signal.connect(self.on_change_state)
            self.thread_train.end_batch_signal.connect(self.on_end_batch)
            self.thread_train.end_epoch_signal.connect(self.on_end_epoch)
            self.thread_train.end_signal.connect(self.on_end_train)

            # Start training
            self.thread_train.start()
        else:
            # Show error message
            error_title = 'Error'
            error_message = '폴더 및 파라미터를 설정해주세요.'
            QMessageBox.critical(self, error_title, error_message, QMessageBox.Ok)

    def on_click_save(self):
        path = QFileDialog.getSaveFileName(self, 'Save model', 'model.pt', 'Pytorch model (*.pt)')[0]
        if path:
            torch.save(self.model, path)
            QMessageBox.information(self, 'Save', '모델 저장에 성공했습니다.', QMessageBox.Ok)

    @pyqtSlot()
    def on_start_train(self):
        self.reset_progress_bar(self.epochs)
        self.progress_bar.setValue(0)
        self.disable_widgets()

    @pyqtSlot(str)
    def on_change_state(self, text):
        if text:
            self.status_bar.showMessage(text)
        else:
            self.status_bar.clearMessage()

    @pyqtSlot(list)
    def on_end_batch(self, losses):
        signal = np.array(losses)
        cv2.normalize(signal, signal, 1, 0, cv2.NORM_MINMAX)
        signal = 1 - signal

        h, w = self.label_graph.height(), self.label_graph.width()
        l = signal.shape[0]
        frame = np.ones((h, w, 3), np.uint8) * 255
        for i in range(l - 1):
            sy = int(signal[i] * h)
            ey = int(signal[i + 1] * h)
            sx = int(i * (w / l))
            ex = int((i + 1) * (w / l))

            cv2.line(frame, (sx, sy), (ex, ey), (0, 0, 255), 2)
        self.set_image(frame, self.label_graph)

    @pyqtSlot()
    def on_end_epoch(self):
        val = self.progress_bar.value()
        self.progress_bar.setValue(val + 1)

    @pyqtSlot(object)
    def on_end_train(self, model):
        self.model = model
        self.reset_progress_bar()
        self.enable_widgets()
        self.button_save.setDisabled(False)
        QMessageBox.about(self, 'Done', '학습이 완료되었습니다.')


class TrainThread(QThread):
    start_signal = pyqtSignal()
    change_state_signal = pyqtSignal(str)
    end_batch_signal = pyqtSignal(list)
    end_epoch_signal = pyqtSignal()
    end_signal = pyqtSignal(object)

    def set_parameters(self, path, batch_size, epochs, lr):
        self.path = path
        self.batch_size = batch_size
        self.epochs = epochs
        self.lr = lr

    def run(self):
        self.start_signal.emit()

        self.change_state_signal.emit('Device setting..')
        self.set_device()

        self.change_state_signal.emit('Train data setting..')
        self.set_train_data()

        self.change_state_signal.emit('Model setting..')
        self.set_model()

        self.change_state_signal.emit('Training..')
        self.train()

        self.change_state_signal.emit('')

    def set_device(self):
        if torch.cuda.is_available():
            self.devices_id = torch.device("cuda:0")
            torch.cuda.set_device(self.devices_id)
        else:
            self.devices_id = torch.device("cpu")

    def set_train_data(self):
        self.train_dataset = datasets.MNIST(root=self.path, train=True, transform=transforms.ToTensor(), download=True)
        self.train_loader = DataLoader(dataset=self.train_dataset, batch_size=self.batch_size, shuffle=True)

    def set_model(self):
        self.model = CNN()
        if torch.cuda.is_available():
            self.model = nn.DataParallel(self.model, device_ids=self.devices_id if type(self.devices_id) == list else [self.devices_id]).cuda()
        self.criterion = torch.nn.CrossEntropyLoss()
        self.optimizer = torch.optim.SGD(self.model.parameters(), lr=self.lr)

    def train(self):
        losses = []
        for epoch in range(self.epochs):
            for i, (images, labels) in enumerate(self.train_loader):
                images = images.to(self.devices_id)
                labels = labels.to(self.devices_id)

                self.optimizer.zero_grad()
                outputs = self.model(images)
                loss = self.criterion(outputs, labels)
                loss.backward()
                self.optimizer.step()

                losses.append(loss.item())
                self.end_batch_signal.emit(losses)
            self.end_epoch_signal.emit()
        self.end_signal.emit(self.model)


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

