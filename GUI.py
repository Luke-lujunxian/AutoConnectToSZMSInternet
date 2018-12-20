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
        #QLineEdit.PasswordEchoOnEdit()
        #Online = QPushButton("Online")
        #Online.clicked.connect(Auto_connect.main())
        self.InputAcu = self.InputAccount
        self.InputPas = self.InputPassword
        self.InputPas.setEchoMode(QLineEdit.Password)
        self.Online.clicked.connect(self.Onlinefun)
        self.Offline.clicked.connect(self.Offlinefun)
        try:
            data = open("Data.dat", 'r')
            lines = data.readlines()
            self.InputAcu.setText(lines[0])
            self.InputPas.setText(lines[1])
        except FileNotFoundError:
            pass
        except IndexError:
            pass




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
            t1.is_alive()
            t1.isAlive()
            self.Threads.append(t1)
        else:
            temp = self.Threads.pop()
            if temp.isAlive():
                print("已启动")
                self.Threads.append(temp)
            else:
                self.Onlinefun()








app = QApplication(sys.argv)
w = MainWindow()
w.move(300,300)

w.show()
sys.exit(app.exec_())
