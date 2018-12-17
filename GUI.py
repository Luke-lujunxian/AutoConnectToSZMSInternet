import sys
from PyQt5.QtWidgets import QApplication, QDialog,QPushButton,QLineEdit
from PyQt5.uic import loadUi
import Auto_connect
import threading
import queue
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


Endevent = threading.Event()
class MainWindow(QDialog):
    Threads = []
    Username = "zhchen"
    Password = "zhchen"
    InputAcu = ""
    InputPas = ""


    def __init__(self, parent=None):
        global browser
        super(QDialog, self).__init__(parent)
        loadUi('Main.ui', self)
        #self.setFixedSize(self.sizeHint())

        #Online = QPushButton("Online")
        #Online.clicked.connect(Auto_connect.main())
        self.InputAcu = self.InputAccount
        self.InputPas = self.InputPassword
        self.Online.clicked.connect(self.Onlinefun)
        self.Offline.clicked.connect(self.Offlinefun)




    def Offlinefun(self):
        Endevent.set()
        if self.Threads.__len__() != 0:
            self.Threads.pop()

    def Onlinefun(self):
        Endevent.clear()
        if self.InputAcu.text().strip().__len__() >0 and self.InputPas.text().strip().__len__() >0:
            self.Username = self.InputAcu.text()
            self.Password = self.InputPas.text()
        #print(username)
        if self.Threads.__len__() == 0:
            t1 = threading.Thread(target=Auto_connect.main,args=(Endevent, self.Username, self.Password))
            t1.start()
            self.Threads.append(t1)
        else:
            print("已启动")








app = QApplication(sys.argv)
w = MainWindow()
w.move(300,300)

w.show()
sys.exit(app.exec_())
