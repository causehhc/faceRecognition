import datetime
import os
import sys
import cv2

from recognition.Recognizer import FaceRecognizer
from backend.db import MySqlHelper

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QTableWidgetItem
from PyQt5.QtWidgets import QApplication, QMainWindow, QUndoStack, QMessageBox, QLabel
from MainUI import Ui_MainWindow
from DataUI import Ui_DataWindow


class MainForm(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        path_h5 = './recognition/data/pictures'
        path_root = './recognition/align/model'
        # path_model = './recognition/data/model'
        path_model = './recognition/data/model_origin'
        self.recognizer = FaceRecognizer(path_h5, path_root, path_model)

        self.sqlHelper = MySqlHelper()

        if not os.path.exists("{}/embeddings.h5".format(path_h5)):
            self.sqlHelper.clear()

        self.sub_win = SubForm(self.sqlHelper)

        # Info
        self.pname = None
        self.psex = None
        self.pimgid = None
        self.pphone = None

        # 摄像头
        self.is_camera_opened = False
        self.old_face_class = None
        self.time_dict = {}

        # 定时器：100ms捕获一帧
        self._timer = QtCore.QTimer(self)
        self._timer.timeout.connect(self._queryFrame)
        self._timer.setInterval(100)

        self._timer2 = QtCore.QTimer(self)
        self._timer2.timeout.connect(self._flashTime)
        self._timer2.setInterval(1000)
        self._timer2.start()

        # connect
        self.pushButton_Camera.clicked.connect(self.func_pushButton_Camera)
        self.pushButton_Search.clicked.connect(self.func_pushButton_Search)
        self.pushButton_InfoRE.clicked.connect(self.func_pushButton_InfoRE)
        self.pushButton_Edit.clicked.connect(self.func_pushButton_Edit)
        self.pushButton_Commit.clicked.connect(self.func_pushButton_Commit)
        self.pushButton_Delete.clicked.connect(self.func_pushButton_Delete)

    @QtCore.pyqtSlot()
    def _queryFrame(self):
        """
        循环捕获图片
        """
        ret, self.frame, face_class = self.recognizer.get_one_shot(self.pushButton_Start.isChecked())
        if self.old_face_class != face_class:  # 优化刷新
            self.old_face_class = face_class
            if face_class:
                self._set_info(face_class)
                now = datetime.datetime.now()
                flag = False
                if face_class not in self.time_dict:
                    self.time_dict[face_class] = now
                    flag = True
                if flag or (now - self.time_dict[face_class]).seconds > 60:  # 10s打卡周期
                    self.time_dict[face_class] = now
                    self.sqlHelper.create_log(face_class, now)
                    self.lineEdit_State.setText("Check in successfully, {}, {}".format(face_class, now))
                    print("Check in successfully, {}, {}".format(face_class, now))
            else:
                if not self.pushButton_Edit.isChecked():
                    self.func_pushButton_InfoRE(force=True)

        img_rows, img_cols, channels = self.frame.shape
        bytesPerLine = channels * img_cols

        cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB, self.frame)
        QImg = QImage(self.frame.data, img_cols, img_rows, bytesPerLine, QImage.Format_RGB888)
        Size = self.label_Camera.size()
        self.label_Camera.setPixmap(QPixmap.fromImage(QImg).scaled(Size, Qt.KeepAspectRatio, Qt.SmoothTransformation))

    @QtCore.pyqtSlot()
    def _flashTime(self):
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.lineEdit_Time.setText(now)

        if self.is_camera_opened:
            state = "Camera_open"
            if self.pushButton_Start.isChecked():
                state = "Face_running..."
        else:
            state = "Camera_close"
        if self.pushButton_Edit.isChecked():
            state = "Edit..."
        self.lineEdit_State.setText(state)

    def _get_info(self):
        self.pname = self.lineEdit_PName.text()
        self.psex = self.lineEdit_PSex.text()
        self.pimgid = self.lineEdit_PImgID.text()
        self.pphone = self.lineEdit_PPhone.text()

    def _set_info(self, face_class):
        if not self.pushButton_Edit.isChecked():
            item = self.sqlHelper.get_info(face_class)
            self.lineEdit_PName.setText(item[0])
            self.lineEdit_PSex.setText(item[1])
            self.lineEdit_PImgID.setText(str(item[2]))
            self.lineEdit_PPhone.setText(item[3])

    def func_pushButton_Camera(self):
        """
        打开和关闭摄像头
        """
        self.is_camera_opened = ~self.is_camera_opened
        if self.is_camera_opened:
            self.pushButton_Camera.setText("Close")
            self._timer.start()
        else:
            self._timer.stop()
            self.label_Camera.setText("Camera")
            self.pushButton_Camera.setText("Open")

    def func_pushButton_Search(self):
        self.sub_win.init_data()
        self.sub_win.show()

    def func_pushButton_InfoRE(self, force=False):
        if force or self.pushButton_Edit.isChecked():
            self.pname = None
            self.psex = None
            self.pimgid = None
            self.pphone = None
            self.lineEdit_PName.clear()
            self.lineEdit_PSex.clear()
            self.lineEdit_PImgID.clear()
            self.lineEdit_PPhone.clear()

    def func_pushButton_Edit(self):
        if self.pushButton_Edit.isChecked():
            self.func_pushButton_InfoRE()
            flag = False
        else:
            flag = True
        self.lineEdit_PName.setReadOnly(flag)
        self.lineEdit_PSex.setReadOnly(flag)
        self.lineEdit_PImgID.setReadOnly(flag)
        self.lineEdit_PPhone.setReadOnly(flag)

    def func_pushButton_Commit(self):
        self._timer.stop()
        if self.is_camera_opened and self.pushButton_Start.isChecked() and self.pushButton_Edit.isChecked():
            self._get_info()
            if None not in [self.pname, self.psex, self.pimgid, self.pphone]:
                ret, frame, face_class = self.recognizer.get_one_shot(True, imgID=self.pimgid)
                self.sqlHelper.update_info([self.pname, self.psex, self.pimgid, self.pphone], face_class)
                self.func_pushButton_InfoRE()
                self.pushButton_Edit.setChecked(False)
                self.func_pushButton_Edit()
        self._timer.start()

    def func_pushButton_Delete(self):
        self._timer.stop()
        if self.is_camera_opened and self.pushButton_Start.isChecked():
            self._get_info()
            if None not in [self.pname, self.psex, self.pimgid, self.pphone]:
                ret, frame, face_class = self.recognizer.get_one_shot(True, imgID=self.pimgid, delete=True)
                self.sqlHelper.del_info([self.pname, self.psex, self.pimgid, self.pphone])
                self.func_pushButton_InfoRE()
                self.pushButton_Edit.setChecked(False)
                self.func_pushButton_Edit()
        self._timer.start()


class SubForm(QMainWindow, Ui_DataWindow):
    def __init__(self, sqlHelper, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.sqlHelper = sqlHelper

        # connect
        self.pushButton_create.clicked.connect(self.func_pushButton_create)
        self.pushButton_search.clicked.connect(self.func_pushButton_search)

    def init_data(self):
        item_list1, item_list2 = self.sqlHelper.get_info_all()
        self.tableWidget_person_info.setRowCount(len(item_list1))
        for i in range(len(item_list1)):
            for j in range(len(item_list1[i])):
                self.tableWidget_person_info.setItem(i, j, QTableWidgetItem(item_list1[i][j]))
        self.tableWidget_report.setRowCount(len(item_list2))
        for i in range(len(item_list2)):
            for j in range(len(item_list2[i])):
                self.tableWidget_report.setItem(i, j, QTableWidgetItem(item_list2[i][j]))

    def func_pushButton_create(self):
        category = self.comboBox_table.currentText()
        item_list = self.sqlHelper.get_log_time(category)
        self.tableWidget_report.setRowCount(0)
        self.tableWidget_report.setRowCount(len(item_list))
        for i in range(len(item_list)):
            for j in range(len(item_list[i])):
                self.tableWidget_report.setItem(i, j, QTableWidgetItem(item_list[i][j]))

    def func_pushButton_search(self):
        category = self.comboBox_search.currentText()
        text = self.lineEdit_search.text()
        item_list = self.sqlHelper.get_log(category, text)
        self.tableWidget_report.setRowCount(0)
        self.tableWidget_report.setRowCount(len(item_list))
        for i in range(len(item_list)):
            for j in range(len(item_list[i])):
                self.tableWidget_report.setItem(i, j, QTableWidgetItem(item_list[i][j]))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainForm()
    win.show()
    res = app.exec_()
    if win.recognizer.commitFlag:
        win.recognizer.save_embedding()
    sys.exit(res)
