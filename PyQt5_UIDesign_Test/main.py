from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import timeUI as ui              #引用UI檔
import time
import os

class Main(QMainWindow, ui.Ui_MainWindow):
    def __init__(self):
         super().__init__()
         self.setupUi(self)
         
         #非可視物件綁定
         # self.timer = QTimer(self)
         # self.timer.timeout.connect(self.run) #當時間到時會執行 run
         # self.timer.start(1000) #啟動 Timer .. 每隔1000ms 會觸發 run
         
         #UI物件綁定
         self.pushButton.clicked.connect(self.ProgramExit)

    #事件處理
    def ProgramExit(self):
        #self.label.setText(time.ctime())
        #print (time.ctime())
        print ('111')
        self.label.setText('111')
        #os._exit(0)

    def run(self):
        self.label.setText(time.ctime())
        

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())