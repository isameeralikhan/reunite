import sys
import requests
import base64
import json
import uuid
import hashlib

from PIL import Image
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap, QImage, QImageReader
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QPushButton, QApplication
from PyQt5.QtWidgets import QInputDialog, QLabel, QLineEdit, QMessageBox, QComboBox

class MobileApp(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Register User")
        self.setFixedSize(400, 400)
        self.icon_path = "../resources/icon.png"
        self.username = None
        self.password = None
        self.role = None
        self.initialize()

    def initialize(self):
        self.setWindowIcon(QtGui.QIcon(self.icon_path))
        self.get_username()
        self.get_password()
        self.get_role()
        
        register_bt = QPushButton("Register", self)
        register_bt.move(150, 280)
        register_bt.clicked.connect(self.register)
        
    def get_username(self):
        self.username_label = QLabel(self)
        self.username_label.setText("username:")
        self.username_label.move(100, 90)
        
        self.user = QLineEdit(self)
        self.user.move(200, 90)
    
    def get_password(self):
        self.password_label = QLabel(self)
        self.password_label.setText("password:")
        self.password_label.move(100, 150)
        
        self.passw = QLineEdit(self)
        self.passw.move(200, 150)
        
    def get_role(self):
        self.role_label = QLabel(self)
        self.role_label.setText("role:")
        self.role_label.move(100, 205)
        
        self.combo_box = QComboBox(self)
 
        # setting geometry of combo box
        self.combo_box.move(200,210)
        self.combo_box.resize(100,20)
        # geek list
        roles = ["RW"]
 
        # adding list of items to combo box
        self.combo_box.addItems(roles)
 
        # creating editable combo box
        self.combo_box.setEditable(False)
        self.combo_box.setStyleSheet("QComboBox"
                                     "{"
                                     "background-color: white;"
                                     "}")
    
    def register(self):
        if not self.passw.text() or not self.user.text() or not self.combo_box.currentText():
            QMessageBox.about(self, "Invalid", "\nPlease fill all entries\t\n")
        else:
            try:
                URL = "http://localhost:8000/register"
                headers = {"Content-Type": "application/json", "Accept": "application/json"}
                print(self.user.text()+" "+self.passw.text()+" "+self.combo_box.currentText())
                ent={}
                ent["username"] = self.user.text()
                ent["password"] = hashlib.sha256(self.passw.text().encode('utf-8')).hexdigest()
                ent["role"] = self.combo_box.currentText()
                res = requests.post(URL, json.dumps(ent), headers=headers)
                if res.status_code == 200:
                    QMessageBox.about(self,"Success", "\nNew user registered successfully\t\n")
                    self.close()
                else:
                    QMessageBox.about(self, "Failed", "\nCan't register\t\nor user already exists\t\n")
            except Exception as e:
                QMessageBox.about(self, "Conenction Error", "\nDatabase is not running\t\n")
        

app = QApplication(sys.argv)
if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    w = MobileApp("exit")
    sys.exit(app.exec())

