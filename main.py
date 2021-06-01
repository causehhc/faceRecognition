import sys

import cv2
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QFileDialog, QMainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow, QUndoStack, QMessageBox, QLabel
from MainUI import Ui_MainWindow
from recognition.run.test import FaceRecognizer


class MainForm(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        path_h5 = './recognition/data/pictures/embeddings.h5'
        path_root = './recognition/align/model'
        path_model = './recognition/data/model_origin'
        self.recognizer = FaceRecognizer(path_h5, path_root, path_model)

        # 摄像头
        self.is_camera_opened = False

        # 定时器：100ms捕获一帧
        self._timer = QtCore.QTimer(self)
        self._timer.timeout.connect(self._queryFrame)
        self._timer.setInterval(100)

        # connect
        self.pushButton_Camera.clicked.connect(self.func_pushButton_Camera)
        self.pushButton_Edit.clicked.connect(self.func_pushButton_Edit)
        self.pushButton_Search.clicked.connect(self.func_pushButton_Search)
        self.pushButton_InfoRE.clicked.connect(self.func_pushButton_InfoRE)
        self.pushButton_Shot.clicked.connect(self.func_pushButton_Shot)
        self.pushButton_Commit.clicked.connect(self.func_pushButton_Commit)
        self.pushButton_ConsoleRE.clicked.connect(self.func_pushButton_ConsoleRE)

    @QtCore.pyqtSlot()
    def _queryFrame(self):
        """
        循环捕获图片
        """
        if self.pushButton_Start.isChecked():
            ret, self.frame = self.recognizer.get_one_shot()
        else:
            ret, self.frame = self.recognizer.get_one_shot_normal()

        img_rows, img_cols, channels = self.frame.shape
        bytesPerLine = channels * img_cols

        cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB, self.frame)
        QImg = QImage(self.frame.data, img_cols, img_rows, bytesPerLine, QImage.Format_RGB888)
        Size = self.label_Camera.size()
        self.label_Camera.setPixmap(QPixmap.fromImage(QImg).scaled(Size, Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def func_pushButton_Camera(self):
        """
        打开和关闭摄像头
        """
        self.is_camera_opened = ~self.is_camera_opened
        if self.is_camera_opened:
            self.pushButton_Camera.setText("Close")
            self._timer.start()
        else:
            self.pushButton_Camera.setText("Open")
            self._timer.stop()
            self.label_Camera.setText("Camera")

    def func_pushButton_Edit(self):
        if self.pushButton_Edit.isChecked():
            self.lineEdit_PName.setReadOnly(False)
            self.lineEdit_PSex.setReadOnly(False)
            self.lineEdit_PPhone.setReadOnly(False)
        else:
            self.lineEdit_PName.setReadOnly(True)
            self.lineEdit_PSex.setReadOnly(True)
            self.lineEdit_PPhone.setReadOnly(True)

    def func_pushButton_Search(self):
        # TODO
        pass

    def func_pushButton_InfoRE(self):
        if self.pushButton_Edit.isChecked():
            self.lineEdit_PName.clear()
            self.lineEdit_PSex.clear()
            self.lineEdit_PPhone.clear()

    def func_pushButton_Shot(self):
        if self.is_camera_opened:
            self._timer.stop()
            img_rows, img_cols, channels = self.frame.shape
            bytesPerLine = channels * img_cols

            cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB, self.frame)
            QImg = QImage(self.frame.data, img_cols, img_rows, bytesPerLine, QImage.Format_RGB888)
            Size = self.label_Camera.size()
            self.label_Camera.setPixmap(QPixmap.fromImage(QImg).scaled(Size, Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def func_pushButton_Commit(self):
        # TODO
        pass

    def func_pushButton_ConsoleRE(self):
        self._timer.start()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainForm()
    win.show()
    sys.exit(app.exec_())
