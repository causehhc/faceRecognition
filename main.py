import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QUndoStack, QMessageBox, QLabel
from ui import Ui_MainWindow


class MyMainForm(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.pushButton.clicked.connect(self.func)

    def func(self):
        print('ss')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_win = MyMainForm()
    my_win.show()
    sys.exit(app.exec_())
