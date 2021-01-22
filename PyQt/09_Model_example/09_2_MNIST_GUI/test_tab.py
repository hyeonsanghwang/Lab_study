import cv2
import torch

from PyQt5 import QtGui
from PyQt5 import uic
from PyQt5.QtWidgets import QFileSystemModel, QFileDialog, QWidget

form_class = uic.loadUiType('ui/test_tab.ui')[0]
class TabTest(QWidget, form_class):
    def __init__(self, status_bar):
        super().__init__()
        self.setupUi(self)

        self.status_bar = status_bar
        self.model = None

        self.set_tree_view()
        self.check_model_loaded()
        self.set_events()

    def set_tree_view(self):
        self.root_path = "../../"
        self.file_model = QFileSystemModel()
        self.file_model.setRootPath(self.root_path)

        self.tree_view.setModel(self.file_model)
        self.tree_view.setRootIndex(self.file_model.index(self.root_path))
        self.tree_view.setColumnHidden(1, True)
        self.tree_view.setColumnHidden(2, True)
        self.tree_view.setColumnHidden(3, True)

    def check_model_loaded(self):
        if self.model is None:
            self.label_state.setText('Not loaded')
        else:
            self.label_state.setText('Loaded')

    def set_events(self):
        self.button_load.clicked.connect(self.on_click_load)
        self.tree_view.clicked.connect(self.on_click_tree_view)

    def on_click_load(self):
        self.status_bar.showMessage('Load model...')

        path = QFileDialog.getOpenFileName(self, 'Select model', '', 'Pytorch model (*.pt)')[0]
        if path:
            self.model = torch.load(path)
            self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
            self.model.eval()
            self.model = self.model.to(self.device)
        self.check_model_loaded()

        self.status_bar.clearMessage()

    def on_click_tree_view(self, index):
        if not self.file_model.isDir(index):
            path = self.file_model.filePath(index)
            image = cv2.imread(path)
            resized = cv2.resize(image, (self.label_image.width(), self.label_image.height()), interpolation=cv2.INTER_AREA)
            self.set_image(resized, self.label_image)

            if self.model is not None:
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                data = torch.from_numpy(gray).float() / 255.0
                data = torch.unsqueeze(torch.unsqueeze(data, 0), 0)
                data = data.to(self.device)

                with torch.no_grad():
                    output = self.model(data)
                    _, pred = torch.max(output.data, 1)
                    pred_number = pred.cpu().numpy()[0]
                    self.label_result.setText(str(pred_number))

    def set_image(self, frame, label):
        image = QtGui.QImage(frame, frame.shape[1], frame.shape[0], frame.shape[1] * 3, QtGui.QImage.Format_BGR888)
        pixmap = QtGui.QPixmap(image)
        label.setPixmap(pixmap)