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
        self.setGeometry(100,100,1280,720)   
        self.chips = 0

        # Put the widgets here
        self.startButton = QPushButton(self.tr("&Start"))       
        self.printerLabel = QLabel("placeholder")
        self.outputLabel = QLabel("placeholder")
        self.selectionCRdo = QRadioButton("Call/check")
        self.selectionRRdo = QRadioButton("Raise")
        self.selectionFRdo = QRadioButton("Fold")
        self.buttonConfirm = QPushButton("Enter")
        self.flop1 = QLabel("card1")
        self.flop2 = QLabel("card2")
        self.flop3 = QLabel("card3")
        self.flop4 = QLabel("card4")
        self.flop5 = QLabel("card5")
        self.hand1 = QLabel("hand1")
        self.hand2 = QLabel("hand2")
        self.potLabel = QLabel("0")
        self.chipLabel = QLabel('0')

        centerLayout = QHBoxLayout()
        centerRow = QHBoxLayout()
        centerLayout.addWidget(self.flop1)
        centerLayout.addWidget(self.flop2)
        centerLayout.addWidget(self.flop3)
        centerLayout.addWidget(self.flop4)
        centerLayout.addWidget(self.flop5)

        self.centerGroup = QGroupBox()
        self.centerGroup.setLayout(centerLayout)
        centerRow.addStretch(1)
        centerRow.addWidget(self.centerGroup)
        centerRow.addWidget(self.potLabel)
        centerRow.addStretch(1)

        handLayout = QHBoxLayout()
        handrow = QHBoxLayout()
        handLayout.addWidget(self.hand1)
        handLayout.addWidget(self.hand2)

        self.handGroup = QGroupBox()
        self.handGroup.setLayout(handLayout)
        handrow.addStretch(3)
        handrow.addWidget(self.handGroup)
        handrow.addWidget(self.chipLabel)
        handrow.addStretch(3)

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

        layout = QVBoxLayout()
        layout.addWidget(self.startButton)
        layout.addWidget(self.printerLabel)
        layout.addStretch(1)
        layout.addLayout(centerRow)
        layout.addStretch(1)
        layout.addLayout(handrow)
        layout.addWidget(self.selectionCRdo)
        layout.addWidget(self.selectionRRdo)
        layout.addWidget(self.selectionFRdo)
        layout.addWidget(self.buttonConfirm)
        

        #layout.addLayout(self.inputLayout)
        self.selectionCRdo.hide()
        self.selectionRRdo.hide()
        self.selectionFRdo.hide()
        self.buttonConfirm.hide()

        self.setLayout(layout)        
        self.setWindowTitle(self.tr("Poker Game"))
        

    def startListener(self):
        # show all of the stuff
        self.thread.listen()
      
    def success(self):
        print("we did it")

    def printer(self):
        if isinstance(window.printvalue, list ):
            if window.printvalue[0]=='2':
                self.hand1.setText(str(window.printvalue[1][0]))
                self.hand2.setText(str(window.printvalue[1][1]))
                chipinfo = window.printvalue[3]
                print(chipinfo)
                if chipinfo[1] == 0:
                    print("small blind")
                    self.chips = int(chipinfo[0] - ((1/3)*int(window.printvalue[2])))
                elif chipinfo[1] == 1:
                    print("big blind")
                    self.chips = int(chipinfo[0] - ((2/3)*int(window.printvalue[2])))
                else:
                    self.chips = int(chipinfo[0])
                self.chipLabel.setText(str(self.chips))
                
            elif window.printvalue[0]=='3':
                self.flop1.setText(str(window.printvalue[1][0]))
                self.flop2.setText(str(window.printvalue[1][1]))
                self.flop3.setText(str(window.printvalue[1][2]))
            elif window.printvalue[0]=='4':
                self.flop4.setText(str(window.printvalue[1]))
            elif window.printvalue[0]=='5':
                self.flop5.setText(str(window.printvalue[1]))

            else:
                printval = str(window.printvalue)
                self.printerLabel.setText(printval)
        else:
            printval = str(window.printvalue)
            self.printerLabel.setText(printval)

    def takeInput(self):
        window.selectionCRdo.show()
        window.selectionRRdo.show()
        window.selectionFRdo.show()
        window.buttonConfirm.show()

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
            window.chips -= self.currentBet
            if window.chips<0:
                window.chips = 0
            window.chipLabel.setText(str(window.chips))
            val = 'C'
        elif window.selectionRRdo.isChecked():
            val = 'R'
        elif window.selectionFRdo.isChecked():
            val = 'F'
        val = pickle.dumps(val)
        window.selectionCRdo.hide()
        window.selectionRRdo.hide()
        window.selectionFRdo.hide()
        window.buttonConfirm.hide()
        self.gamesocket.send(val)
        
        

    def run(self):      
        window.printvalue = "connecting..."
        
        print("rerun")
        self.printTime.emit()
        self.gamesocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        """for row in serverList:
            if row[0]  == serverNum:
                host = row[2]
                break"""
        port = 6060         # port forwarded this on servers router
        self.gamesocket.connect(("81.135.23.12", port))
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
                    try:
                        pot = int(data[1])
                        pickled = pickle.dumps("None")
                        self.gamesocket.send(pickled)
                        window.potLabel.setText(str(pot))
                    except Exception as error:
                        print(error)
                        if len(data) == 3:
                            self.currentBet = int(data[2])
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
        window.selectionCRdo.show()
        window.selectionRRdo.show()
        window.selectionFRdo.show()
        window.buttonConfirm.show()

app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec_())