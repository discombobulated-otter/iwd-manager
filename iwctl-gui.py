import sys
from PyQt6.QtWidgets import QLabel,QPushButton,QTextEdit,QApplication,QWidget,QSlider
import subprocess
import re
class appl(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(400,400,600,400)
        self.setWindowTitle("IWD Manager")
        
        self.label= QLabel("Scan Networks", self)
        self.label.setGeometry(0,10,100,25)
        
        
        self.button = QPushButton("Scan",self)    
        self.button.setGeometry(150,10,50,25)
        self.button.clicked.connect(self.cmd)
        
        self.text=QTextEdit(self)
        self.text.setGeometry(10,50,600,350)
    def cmd(self):
        self.text.autoFormatting()
        terminal_command = subprocess.run(["iwctl",'station',"wlan0","get-networks"],text=True,capture_output=True,check=True)
        out = terminal_command.stdout
        output= re.sub(r'\x1b\[[0-9;]*m', '', out)
        self.text.setPlainText(output)
        
    def buttons(self):
        #basically I will take input from that regex formatted fuction then run a loop to make multiple buttons and iterate that regex to name those buttons.
        pass
        
        
    
if __name__=='__main__':   
    app= QApplication(sys.argv)   
    wi=appl()
    wi.show()
    sys.exit(app.exec())