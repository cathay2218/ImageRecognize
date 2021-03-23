from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import timeUI as ui              #引用UI檔
import time

class Main(QMainWindow, ui.Ui_MainWindow):
    def __init__(self):
         super().__init__()
         self.setupUi(self)
         
         
         #物件綁定
         self.pushButton.clicked.connect(self.show_time)

    #事件處理
    def show_time(self):
        self.label.setText(time.ctime())
        print (time.ctime())

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())