import sys
from iwd_ui import *
from PyQt6.QtWidgets import *
import subprocess

class appl(QMainWindow, Ui_MainWindow):
    
     def __init__(self):
        super().__init__()
        
        self.setupUi(self)
        
        self.pushButton_2.clicked.connect(self.scan)
        
     def scan(self):
         command = "iwctl station wlan0 get-networks > scanned.txt"

         result = subprocess.run(command,check=True)
        
        
        
    