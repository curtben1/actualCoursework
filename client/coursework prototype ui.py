import math, random, sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import socket
import pickle
from sys import getsizeof

# note: can use window properties to pass variables betwwen 

class Window(QWidget):
    out = pyqtSignal()
    def __init__(self, parent = None):
        self.netInfo = 0
        QWidget.__init__(self, parent)        
        

        # Put the widgets here
        self.startButton = QPushButton(self.tr("&Start"))       
        self.printerLabel = QLabel("placeholder")
        self.outputLabel = QLabel("placeholder")
        self.selectionCRdo = QRadioButton("Call/check")
        self.selectionRRdo = QRadioButton("Raise")
        self.selectionFRdo = QRadioButton("Fold")
        self.buttonConfirm = QPushButton("Enter")

        self.radioGroup = QButtonGroup()
        self.radioGroup.addButton(self.selectionCRdo)
        self.radioGroup.addButton(self.selectionRRdo)
        self.radioGroup.addButton(self.selectionFRdo)
        self.radioGroup.addButton(self.buttonConfirm)

        self.thread = Worker(self)

        self.thread.finished.connect(self.threadDied)
        self.startButton.clicked.connect(self.startListener)
        self.thread.output.connect(self.success)
        self.thread.printTime.connect(self.printer)
        


        layout = QGridLayout()
        layout.addWidget(self.startButton)
        layout.addWidget(self.printerLabel)
        layout.addWidget(self.selectionCRdo)
        layout.addWidget(self.selectionRRdo)
        layout.addWidget(self.selectionFRdo)
        layout.addWidget(self.buttonConfirm)

        #layout.addLayout(self.inputLayout)

        self.setLayout(layout)        
        self.setWindowTitle(self.tr("Simple Threading Example"))
        

    def startListener(self):
        # show all of the stuff
        self.thread.listen()
      
    def success(self):
        print("we did it")



    def printer(self):
        self.printerLabel.setText(window.printvalue)

    def takeInput(self):
        self.radioGroup.show()

    def threadDied(self):
        pass
        # ran when thread dies, use as when quit game

class Worker(QThread):
    output = pyqtSignal()       # declare signals
    printTime = pyqtSignal()

    def __init__(self,window , parent = None):
        QThread.__init__(self, parent)
        self.exiting = False
        window.buttonConfirm.clicked.connect(self.getInput)

    def __del__(self):    
        self.exiting = True
        self.wait()

    def listen(self):    
        self.start()    

    def getInput(self):
        if window.selectionCRdo.isChecked():
            val = 'C'
        elif window.selectionRRdo.isChecked():
            val = 'R'
        elif window.selectionFRdo.isChecked():
            val = 'F'
        val = pickle.dumps(val)
        self.gamesocket.send(val)
        
        

    def run(self):      
        window.printvalue = "connecting..."
        self.printTime.emit()
        self.gamesocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        """for row in serverList:
            if row[0]  == serverNum:
                host = row[2]
                break"""
        port = 6060         # port forwarded this on servers router
        self.gamesocket.connect(("86.128.35.53", port))
        playerInfo = ["username", "playerNum"]  ## use actual info here
        msg = pickle.dumps(playerInfo)
        self.gamesocket.send(msg)
        while True: 
            
            data2 = self.gamesocket.recv(4096)
            if data2:
                data2 = pickle.loads(data2)
                if isinstance(data2, list):
                    print(data2)
                    break   # here for testing
                    start = input("do you want to start the game now (YES/OTHER)")
                    if start  == "YES":
                        msg =  pickle.dumps(start)
                        self.gamesocket.send(msg)
                else:
                    print(data2)
                    print("game starting")
                    break
        self.gameLoop()


    def gameLoop(self):    
        while True:
            data = self.gamesocket.recv(1024)
            data = pickle.loads(data)   # http://acbl.mybigcommerce.com/52-playing-cards/ connect incoming data to labels with these cards

            try:
                data = data.split('#')
                if data[0]== '1':
                    if len(data) == 3:
                        window.printvalue = "the current bet to call is "+  str(data[2])
                        self.printTime.emit()
                    self.takeInput()
                else:
                    window.printvalue = data[1]
                    self.printTime.emit()
            except:
                window.printvalue = data
                self.printTime.emit()
                if data  == "game over":
                    return "Game Over" 
    
    def testPrint(self):
        print("success")

    def takeInput(self):
        window.radioGroup.show()


app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec_())