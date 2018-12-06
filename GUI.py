import sys
from PyQt5.QtWidgets import QApplication, QDialog,QPushButton
from PyQt5.uic import loadUi
import Auto_connect
import threading
class MainWindow(QDialog):
    def __init__(self, parent=None):
        super(QDialog, self).__init__(parent)
        loadUi('Main.ui', self)
        #self.setFixedSize(self.sizeHint())

        #Online = QPushButton("Online")
        #Online.clicked.connect(Auto_connect.main())
        self.Online.clicked.connect(self.Onlinefun)

    @staticmethod
    def Onlinefun():
        t1 = threading.Thread(target=Auto_connect.main)
        t1.start()
       # print(1)


app = QApplication(sys.argv)
w = MainWindow()
w.move(300,300)

w.show()
sys.exit(app.exec_())
